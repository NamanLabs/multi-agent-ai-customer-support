"""
MongoDB connection + Conversation Memory (Module 8) + basic Analytics
queries (Module 9, bonus).

Set MONGO_URI env var, e.g.:
  export MONGO_URI="mongodb+srv://<user>:<pass>@cluster.mongodb.net/techmart"
Defaults to local MongoDB for development if not set.
"""
import os
import datetime
from pymongo import MongoClient

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.environ.get("MONGO_DB_NAME", "techmart_support")

_client = None
_db = None


def get_db():
    global _client, _db
    if _db is None:
        _client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        _db = _client[DB_NAME]
    return _db


# ---------- Conversation Memory (Module 8) ----------

def save_message(session_id: str, user_id: str, user_message: str,
                  ai_response: str, agents_invoked: list[str], escalated: bool,
                  response_time_ms: float = None):
    db = get_db()
    db.conversations.insert_one({
        "session_id": session_id,
        "user_id": user_id,
        "user_message": user_message,
        "ai_response": ai_response,
        "agents_invoked": agents_invoked,
        "escalated": escalated,
        "response_time_ms": response_time_ms,
        "satisfaction_score": None,  # set later via rate_message()
        "timestamp": datetime.datetime.utcnow(),
    })


def rate_message(session_id: str, message_timestamp, satisfaction_score: int):
    """Lets the frontend submit a 1-5 satisfaction rating for a specific
    AI response after the fact (e.g. thumbs up/down on a message)."""
    db = get_db()
    db.conversations.update_one(
        {"session_id": session_id, "timestamp": message_timestamp},
        {"$set": {"satisfaction_score": satisfaction_score}},
    )


def get_session_history(session_id: str, limit: int = 50) -> list[dict]:
    db = get_db()
    cursor = (
        db.conversations.find({"session_id": session_id}, {"_id": 0})
        .sort("timestamp", 1)
        .limit(limit)
    )
    return list(cursor)


def get_user_sessions(user_id: str) -> list[str]:
    db = get_db()
    return db.conversations.distinct("session_id", {"user_id": user_id})


# ---------- Analytics (Module 9, bonus) ----------

def get_analytics_summary() -> dict:
    db = get_db()
    total_conversations = db.conversations.count_documents({})
    total_escalated = db.conversations.count_documents({"escalated": True})

    pipeline = [
        {"$unwind": "$agents_invoked"},
        {"$group": {"_id": "$agents_invoked", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
    ]
    agent_usage = {doc["_id"]: doc["count"] for doc in db.conversations.aggregate(pipeline)}

    # Average response time (ms) across all conversations that recorded one
    response_time_pipeline = [
        {"$match": {"response_time_ms": {"$ne": None}}},
        {"$group": {"_id": None, "avg_response_time_ms": {"$avg": "$response_time_ms"}}},
    ]
    rt_result = list(db.conversations.aggregate(response_time_pipeline))
    avg_response_time_ms = round(rt_result[0]["avg_response_time_ms"], 1) if rt_result else None

    # Average satisfaction score, out of the messages that were actually rated
    satisfaction_pipeline = [
        {"$match": {"satisfaction_score": {"$ne": None}}},
        {"$group": {"_id": None, "avg_score": {"$avg": "$satisfaction_score"}, "count": {"$sum": 1}}},
    ]
    sat_result = list(db.conversations.aggregate(satisfaction_pipeline))
    avg_satisfaction_score = round(sat_result[0]["avg_score"], 2) if sat_result else None
    rated_count = sat_result[0]["count"] if sat_result else 0

    return {
        "total_conversations": total_conversations,
        "total_escalated": total_escalated,
        "agent_usage": agent_usage,
        "avg_response_time_ms": avg_response_time_ms,
        "avg_satisfaction_score": avg_satisfaction_score,
        "rated_conversations": rated_count,
    }
