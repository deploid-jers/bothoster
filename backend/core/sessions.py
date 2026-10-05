from fastapi import Response
from redis.asyncio import Redis
import secrets

from settings.setting import SESSION_TTL, DEBUG
import json

async def generate_session():
    return secrets.token_urlsafe(32)

async def create_session(user_id: str, session_date: dict, response: Response, redis: Redis):
    session_id = await generate_session()
    
    await redis.set(
        f"session:{session_id}",
        json.dumps(session_date),
        ex=SESSION_TTL
    )

    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        secure=not DEBUG,
        samesite="lax",
        max_age=SESSION_TTL,
        path="/",
    )