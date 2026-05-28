from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text

from app.core.database import Base


class NativeCall(Base):
    __tablename__ = 'native_calls'

    id = Column(Integer, primary_key=True)
    call_id = Column(String(64), unique=True, index=True, nullable=False)
    caller_id = Column(Integer, nullable=False, index=True)
    receiver_id = Column(Integer, nullable=False, index=True)
    mode = Column(String(20), nullable=False)
    channel = Column(String(120), nullable=False)
    status = Column(String(20), nullable=False, default='ringing')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class NativeCallEvent(Base):
    __tablename__ = 'native_call_events'

    id = Column(Integer, primary_key=True)
    call_id = Column(String(64), ForeignKey('native_calls.call_id'), nullable=False, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    event_type = Column(String(20), nullable=False)
    payload_json = Column(Text, default='{}')
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
