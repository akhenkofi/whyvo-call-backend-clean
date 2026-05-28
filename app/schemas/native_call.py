from datetime import datetime
from typing import List, Literal, Optional

from pydantic import BaseModel, Field


class InviteRequest(BaseModel):
    callerId: int
    receiverId: int
    mode: Literal['audio', 'video']
    channel: str = Field(min_length=1, max_length=120)


class NativeCallResponse(BaseModel):
    callId: str
    callerId: int
    receiverId: int
    mode: str
    channel: str
    status: str
    createdAt: datetime


class PollEventResponse(BaseModel):
    id: int
    callId: str
    userId: int
    eventType: str
    payload: dict
    createdAt: datetime


class PollResponse(BaseModel):
    events: List[PollEventResponse]


class AcceptRequest(BaseModel):
    callId: str
    userId: int


class DeclineRequest(BaseModel):
    callId: str
    userId: int


class EndRequest(BaseModel):
    callId: str
    userId: int


class ActionResponse(BaseModel):
    ok: bool
    callId: str
    status: str


class AgoraTokenResponse(BaseModel):
    appId: str
    channel: str
    uid: int
    token: str
    expiresAt: int
