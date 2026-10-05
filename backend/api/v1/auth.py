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

from schemas.auth import *
from redis_client.redis_client import get_redis
from database.connection import get_db
from database.models.users import Users
from core.security import hash_password, verify_password
from core.sessions import generate_session
from api.dependencies import get_current_user, rate_limit_by_ip
from services.auth import *
from settings.setting import DEBUG, SESSION_TTL


router = APIRouter(prefix="/v1/auth", tags=['API Auth'])


@router.post("/registration", status_code=status.HTTP_201_CREATED, dependencies=[Depends(rate_limit_by_ip("register", 20, 900))])
async def registration_user(
    data: RegistrationRequest, 
    db: AsyncSession = Depends(get_db)
    ):

     # TODO Сделать RegisterResponse
    result = await register_user_service(data.username, data.email, data.password, db)
    return {"status": result is not None, "data": result}



@router.post("/login", response_model=LoginResponse, status_code=200, dependencies=[Depends(rate_limit_by_ip("login", 20, 9020))])
async def login_user(
    data: LoginRequest,
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis)
):

    user = await login_user_service(data.login, data.password, response, db, redis, request)
    return LoginResponse(username=user.username, email=user.email)



@router.post("/logout")
async def logout(
    request: Request,
    response: Response,
    redis: Redis = Depends(get_redis),
    user: Users = Depends(get_current_user)
):

    result = await logout_user_server(request, response, redis)

    return result


@router.get("/me", response_model=MeResponse, status_code=200)
async def me(user: Users = Depends(get_current_user)):
    return {"username": user.username, "email": user.email}


@router.post("/verify-email", response_model=None, status_code=200)
async def verify_email(data: VeriryEmailRequest, db = Depends(get_db)):
    email = str(data.email).strip()
    existing_user = await auth_by_username_or_email(db, email)

    if existing_user is None:
        raise NotFoundException("Invalid user")

    # TODO Здесь будет генерировать токен, и сохранять его в Redis под verify-token:{token}:user_id

    result = await send_verify_mail(existing_user.email)
    if result is None or result is False:
        raise ServerBadGetwayException("Ошибка при работе с сервисом по отправке mail")

    return {"status": True, "message": "Письмо на почту отправлено"}
