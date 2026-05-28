import json
import logging
import time
import uuid
from datetime import datetime

from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.native_call import NativeCall, NativeCallEvent

logger = logging.getLogger(__name__)

try:
    from agora_token_builder import RtcTokenBuilder
except Exception:  # pragma: no cover
    RtcTokenBuilder = None


def _log(marker: str, **extra):
    logger.info('%s %s', marker, json.dumps(extra, default=str))


def create_invite(db: Session, caller_id: int, receiver_id: int, mode: str, channel: str):
    call_id = f'whyvo-call-{uuid.uuid4().hex[:16]}'
    call = NativeCall(call_id=call_id, caller_id=caller_id, receiver_id=receiver_id, mode=mode, channel=channel, status='ringing')
    db.add(call)
    db.flush()
    event = NativeCallEvent(call_id=call.call_id, user_id=receiver_id, event_type='invite', payload_json=json.dumps({'callerId': caller_id, 'receiverId': receiver_id, 'mode': mode, 'channel': channel, 'status': 'ringing'}))
    db.add(event)
    db.commit()
    db.refresh(call)
    _log('WHYVO_NATIVE_BACKEND_INVITE_STORED', callId=call.call_id, callerId=caller_id, receiverId=receiver_id, mode=mode)
    return call


def poll_events(db: Session, user_id: int):
    items = db.query(NativeCallEvent).filter(NativeCallEvent.user_id == user_id).order_by(NativeCallEvent.created_at.asc()).all()
    _log('WHYVO_NATIVE_BACKEND_POLL_HIT', userId=user_id, eventCount=len(items))
    return items


def _mutate_call(db: Session, call_id: str, user_id: int, next_status: str, marker: str):
    call = db.query(NativeCall).filter(NativeCall.call_id == call_id).first()
    if not call:
        raise ValueError('Call not found')
    call.status = next_status
    counterpart = call.receiver_id if user_id == call.caller_id else call.caller_id
    event = NativeCallEvent(call_id=call.call_id, user_id=counterpart, event_type=next_status, payload_json=json.dumps({'callId': call.call_id, 'userId': user_id, 'status': next_status, 'channel': call.channel}))
    db.add(event)
    db.commit()
    _log(marker, callId=call.call_id, userId=user_id, status=next_status)
    return call


def accept_call(db: Session, call_id: str, user_id: int):
    return _mutate_call(db, call_id, user_id, 'accepted', 'WHYVO_NATIVE_BACKEND_ACCEPT_STORED')


def decline_call(db: Session, call_id: str, user_id: int):
    return _mutate_call(db, call_id, user_id, 'declined', 'WHYVO_NATIVE_BACKEND_DECLINE_STORED')


def end_call(db: Session, call_id: str, user_id: int):
    return _mutate_call(db, call_id, user_id, 'ended', 'WHYVO_NATIVE_BACKEND_END_STORED')


def build_agora_token(channel: str, uid: int):
    app_id = str(settings.WHYVO_AGORA_APP_ID or '').strip()
    certificate = str(settings.WHYVO_AGORA_APP_CERTIFICATE or '').strip()
    if not app_id or not certificate:
        raise ValueError('Agora credentials are not configured')
    if RtcTokenBuilder is None:
        raise ValueError('Agora token builder is unavailable')
    now = int(time.time())
    expires_at = now + 3600
    role = 1
    token = RtcTokenBuilder.buildTokenWithUid(app_id, certificate, channel, int(uid), role, expires_at)
    _log('WHYVO_NATIVE_BACKEND_TOKEN_OK', channel=channel, uid=uid, expiresAt=expires_at)
    return {'appId': app_id, 'channel': channel, 'uid': int(uid), 'token': token, 'expiresAt': expires_at}
