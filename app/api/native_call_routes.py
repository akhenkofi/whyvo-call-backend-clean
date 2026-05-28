import json
import logging

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.native_call import AcceptRequest, ActionResponse, AgoraTokenResponse, DeclineRequest, EndRequest, InviteRequest, NativeCallResponse, PollEventResponse, PollResponse
from app.services.native_call_service import accept_call, build_agora_token, create_invite, decline_call, end_call, poll_events

router = APIRouter(prefix='/api/v1/whyvo-native-call', tags=['whyvo-native-call'])
logger = logging.getLogger(__name__)


@router.post('/invite', response_model=NativeCallResponse)
def invite(payload: InviteRequest, db: Session = Depends(get_db)):
    try:
        call = create_invite(db, payload.callerId, payload.receiverId, payload.mode, payload.channel)
        return NativeCallResponse(callId=call.call_id, callerId=call.caller_id, receiverId=call.receiver_id, mode=call.mode, channel=call.channel, status=call.status, createdAt=call.created_at)
    except Exception as exc:
        logger.exception('WHYVO_NATIVE_BACKEND_ERROR invite')
        raise HTTPException(status_code=400, detail=str(exc))


@router.get('/poll', response_model=PollResponse)
def poll(user_id: int = Query(...), db: Session = Depends(get_db)):
    try:
        items = poll_events(db, user_id)
        return PollResponse(events=[PollEventResponse(id=item.id, callId=item.call_id, userId=item.user_id, eventType=item.event_type, payload=json.loads(item.payload_json or '{}'), createdAt=item.created_at) for item in items])
    except Exception as exc:
        logger.exception('WHYVO_NATIVE_BACKEND_ERROR poll')
        raise HTTPException(status_code=400, detail=str(exc))


@router.post('/accept', response_model=ActionResponse)
def accept(payload: AcceptRequest, db: Session = Depends(get_db)):
    try:
        call = accept_call(db, payload.callId, payload.userId)
        return ActionResponse(ok=True, callId=call.call_id, status=call.status)
    except Exception as exc:
        logger.exception('WHYVO_NATIVE_BACKEND_ERROR accept')
        raise HTTPException(status_code=400, detail=str(exc))


@router.post('/decline', response_model=ActionResponse)
def decline(payload: DeclineRequest, db: Session = Depends(get_db)):
    try:
        call = decline_call(db, payload.callId, payload.userId)
        return ActionResponse(ok=True, callId=call.call_id, status=call.status)
    except Exception as exc:
        logger.exception('WHYVO_NATIVE_BACKEND_ERROR decline')
        raise HTTPException(status_code=400, detail=str(exc))


@router.post('/end', response_model=ActionResponse)
def end(payload: EndRequest, db: Session = Depends(get_db)):
    try:
        call = end_call(db, payload.callId, payload.userId)
        return ActionResponse(ok=True, callId=call.call_id, status=call.status)
    except Exception as exc:
        logger.exception('WHYVO_NATIVE_BACKEND_ERROR end')
        raise HTTPException(status_code=400, detail=str(exc))


@router.get('/agora-token', response_model=AgoraTokenResponse)
def agora_token(channel: str = Query(...), uid: int = Query(...)):
    try:
        data = build_agora_token(channel, uid)
        return AgoraTokenResponse(**data)
    except Exception as exc:
        logger.exception('WHYVO_NATIVE_BACKEND_ERROR token')
        raise HTTPException(status_code=400, detail=str(exc))
