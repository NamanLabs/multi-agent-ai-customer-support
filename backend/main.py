"""
Main FastAPI application for the Multi-Agent AI Customer Support Assistant.

Run: uvicorn backend.main:app --reload --port 8000
"""
from dotenv import load_dotenv
load_dotenv()

import time
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from backend.models.schemas import (
    RegisterRequest, LoginRequest, ChatRequest, ChatResponse, SessionHistoryResponse,
    RateMessageRequest,
)
from backend.database import auth as auth_db
from backend.database import mongo
from backend.agents.router import route_query

app = FastAPI(title="TechMart Multi-Agent Customer Support API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten this to your frontend URL before production deployment
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer(auto_error=False)


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Optional auth: chat works for guests too, but returns user info if a
    valid token is provided. Keeps the demo usable without forcing login."""
    if credentials is None:
        return None
    try:
        return auth_db.decode_access_token(credentials.credentials)
    except ValueError:
        return None


# ---------- Module 1: Authentication ----------

@app.post("/auth/register")
def register(req: RegisterRequest):
    try:
        user = auth_db.register_user(req.email, req.password, req.name)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/auth/login")
def login(req: LoginRequest):
    try:
        return auth_db.authenticate_user(req.email, req.password)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


# ---------- Module 2/3/4/5/7: Chat (Intent Detection -> Router -> Agents -> RAG) ----------

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest, current_user=Depends(get_current_user)):
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    start_time = time.perf_counter()
    result = route_query(req.message)
    response_time_ms = round((time.perf_counter() - start_time) * 1000, 1)

    user_id = current_user["sub"] if current_user else req.user_id

    # Module 8: persist to conversation memory
    try:
        mongo.save_message(
            session_id=req.session_id,
            user_id=user_id,
            user_message=req.message,
            ai_response=result["final_response"],
            agents_invoked=result["agents_invoked"],
            escalated=result["escalated"],
            response_time_ms=response_time_ms,
        )
    except Exception:
        # Don't fail the chat response if MongoDB is unreachable in dev;
        # log this properly in production instead of silently passing.
        pass

    return ChatResponse(
        response=result["final_response"],
        detected_intents=result["detected_intents"],
        agents_invoked=result["agents_invoked"],
        escalated=result["escalated"],
        confidence=result["confidence"],
    )


# ---------- Module 8: Conversation history ----------

@app.get("/sessions/{session_id}/history", response_model=SessionHistoryResponse)
def session_history(session_id: str):
    messages = mongo.get_session_history(session_id)
    return SessionHistoryResponse(session_id=session_id, messages=messages)


@app.post("/sessions/{session_id}/rate")
def rate_message(session_id: str, req: RateMessageRequest):
    """Lets the frontend submit a 1-5 satisfaction rating (e.g. thumbs up/down,
    or a star rating) for a specific AI response, feeding Module 9 analytics."""
    if not 1 <= req.satisfaction_score <= 5:
        raise HTTPException(status_code=400, detail="satisfaction_score must be between 1 and 5.")
    mongo.rate_message(session_id, req.message_timestamp, req.satisfaction_score)
    return {"status": "ok"}


# ---------- Module 9: Analytics Dashboard (bonus) ----------

@app.get("/analytics/summary")
def analytics_summary():
    return mongo.get_analytics_summary()


@app.get("/health")
def health():
    return {"status": "ok"}
