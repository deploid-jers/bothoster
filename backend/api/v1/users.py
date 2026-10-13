from fastapi import (
    APIRouter, 
    Request, 
    Response, 
    Depends, 
    HTTPException,
    status)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
import json

from redis.asyncio import Redis
from services.user import *
from schemas.user import *
from redis_client.redis_client import get_redis
from database.connection import get_db
from database.models.users import Users
from core.security import hash_password, verify_password
from core.sessions import generate_session
from api.dependencies import get_current_user

router = APIRouter(prefix="/v1/user", tags=['API User'])

@router.get("/me", response_model=MeResponse, status_code=200)
async def me(user: Users = Depends(get_current_user)):
    return {
        "username": user.username, 
        "email": user.email,
        "is_verified": user.is_verified,
        }


@router.post("/email/verify", status_code=200) # TODO Сделать жесткий RATE LIMIT
async def verify_email(
    background_tasks: BackgroundTasks,
    user = Depends(get_current_user), 
    redis: Redis = Depends(get_redis)
    ):

    await verify_email_user_service(user, redis, background_tasks)

    return {"message": "Successfully"}



@router.post("/email/confirm", status_code=200) # TODO Сделать жесткий RATE LIMIT
async def confirm_email(
    data: RequestConfimEmail,
    redis: Redis = Depends(get_redis),
    db: AsyncSession = Depends(get_db),
    ):

    token = data.token

    result = await confim_email_user_service(token, db, redis)

    return result
    
