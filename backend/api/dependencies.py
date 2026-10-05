from fastapi import Depends, HTTPException, Request, status
import redis.asyncio as aioredis
from redis.exceptions import RedisError
from sqlalchemy.ext.asyncio import AsyncSession
import json


from redis_client.redis_client import get_redis
from database.connection import get_db
from database.models.users import Users
from core.exceptions import RateLimitExceeded, ServerBadGetwayException, NotFoundException, UnauthorizedException

async def get_current_user(
        request: Request, 
        redis: aioredis.Redis = Depends(get_redis),
        db: AsyncSession = Depends(get_db)
    ):
    session_id = request.cookies.get("session_id")

    if not session_id:
        raise UnauthorizedException("Not authentificated")


    session_data = await redis.get(f"session:{session_id}")

    if session_data is None:
        raise UnauthorizedException("Session expired")

    
    session_data = json.loads(session_data)

    user = await Users.get(db, id=session_data.get("user_id"))

    if user is None:
        raise UnauthorizedException("Invalid user")
    
    return user


# ========= Rate Limits ===========

async def rate_limit_hit(redis, key, window):
    try:
        async with redis.pipeline(transaction=True) as pipe:
            pipe.incr(key)
            pipe.expire(key, window, nx=True)
            pipe.ttl(key)
            ip_attempts, _, ttl = await pipe.execute()
            return ip_attempts, ttl
    except RedisError:
        raise ServerBadGetwayException("Redis error!")


def rate_limit_by_ip(
        scope: str,
        limit: int,
        window: int
):
    async def dependency(
        request: Request,
        redis: aioredis.Redis = Depends(get_redis),
    ):

        client_ip = request.client.host
        key = f"rl:{scope}:ip:{client_ip}"

        ip_attempts, ttl = await rate_limit_hit(redis, key, window)

        if ip_attempts > limit:
            raise RateLimitExceeded(retry_after=ttl)
    
    return dependency
