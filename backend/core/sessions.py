from fastapi import Response, Request
from redis.asyncio import Redis
from redis.exceptions import RedisError
import secrets

from settings.setting import SESSION_TTL, DEBUG
from core.exceptions import ServerBadGetwayException
import json


async def generate_session():
    return secrets.token_urlsafe(32)


async def get_session_from_req(request: Request):
    return request.cookies.get("session_id")


async def create_session(user_id: str, session_date: dict, response: Response, redis: Redis):
    session_id = await generate_session()

    try:
        async with redis.pipeline(transaction=True) as pipe:
            pipe.set(f"session:{session_id}", json.dumps(session_date), ex=SESSION_TTL)
            pipe.sadd(f"user_sessions:{user_id}", session_id)
            pipe.expire(f"user_sessions:{user_id}", SESSION_TTL) # TODO Узнать как на какие сессии распространяется TTL тут
            await pipe.execute()

    except RedisError:
        raise ServerBadGetwayException("Redis error!")

    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        secure=not DEBUG,
        samesite="lax",
        max_age=SESSION_TTL,
        path="/",
    )


async def destroy_session(session_id: str, user_id: str, redis: Redis, response: Response):
    try:
        async with redis.pipeline(transaction=True) as pipe:
            pipe.delete(f"session:{session_id}")
            pipe.srem(f"user_sessions:{user_id}", session_id)
            await pipe.execute()

    except RedisError:
        raise ServerBadGetwayException("Redis error!")

    response.delete_cookie(
        key="session_id",
        path="/",
        httponly=True,
        secure=not DEBUG,
        samesite="lax",
    )


async def destroy_all_sessions(user_id: str, redis: Redis, except_sid: str = None):
    try:
        sids = await redis.smembers(f"user_sessions:{user_id}")
        to_kill = [sid for sid in sids if sid != except_sid]
        if to_kill:
            async with redis.pipeline(transaction=True) as pipe:
                for sid in to_kill:
                    pipe.delete(f"session:{sid}")
                pipe.srem(f"user_sessions:{user_id}", *to_kill)
                await pipe.execute()


    except RedisError:
        raise ServerBadGetwayException("Redis error!")