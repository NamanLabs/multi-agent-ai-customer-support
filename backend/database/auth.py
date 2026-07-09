"""
Module 1: User Authentication (register, login, session management via JWT)
"""
import os
import datetime
from passlib.context import CryptContext
from jose import jwt, JWTError
from backend.database.mongo import get_db

SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "dev-secret-change-in-production")
ALGORITHM = "HS256"
TOKEN_EXPIRY_HOURS = 24

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def register_user(email: str, password: str, name: str) -> dict:
    db = get_db()
    if db.users.find_one({"email": email}):
        raise ValueError("A user with this email already exists.")

    hashed_pw = pwd_context.hash(password)
    user_doc = {
        "email": email,
        "name": name,
        "password_hash": hashed_pw,
        "created_at": datetime.datetime.utcnow(),
    }
    result = db.users.insert_one(user_doc)
    return {"user_id": str(result.inserted_id), "email": email, "name": name}


def authenticate_user(email: str, password: str) -> dict:
    db = get_db()
    user = db.users.find_one({"email": email})
    if not user or not pwd_context.verify(password, user["password_hash"]):
        raise ValueError("Invalid email or password.")

    token = create_access_token(str(user["_id"]), email)
    return {"access_token": token, "token_type": "bearer", "user_id": str(user["_id"]), "name": user["name"]}


def create_access_token(user_id: str, email: str) -> str:
    expire = datetime.datetime.utcnow() + datetime.timedelta(hours=TOKEN_EXPIRY_HOURS)
    payload = {"sub": user_id, "email": email, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise ValueError("Invalid or expired token.")
