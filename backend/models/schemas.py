from pydantic import BaseModel, EmailStr
from typing import Optional
import datetime


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    name: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class ChatRequest(BaseModel):
    message: str
    session_id: str
    user_id: Optional[str] = "guest"


class ChatResponse(BaseModel):
    response: str
    detected_intents: list[str]
    agents_invoked: list[str]
    escalated: bool
    confidence: float


class SessionHistoryResponse(BaseModel):
    session_id: str
    messages: list[dict]


class RateMessageRequest(BaseModel):
    message_timestamp: datetime.datetime
    satisfaction_score: int
