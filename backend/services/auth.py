import os, re, json
from fastapi_mail import FastMail, MessageSchema, MessageType
from fastapi import HTTPException, status, Response, Request
from starlette.concurrency import run_in_threadpool
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from database.models.users import Users
from settings.setting import conf

from api.dependencies import get_current_user, rate_limit_hit
from utils.auth import login_key
from core.exceptions import *
from schemas.auth import *
from database.models.users import Users
from core.security import hash_password, verify_password, DUMMY_HASH
from core.sessions import generate_session, create_session
from settings.setting import SESSION_TTL, DEBUG

async def auth_by_username_or_email(db, data):
    pattern = r"^[\w\.-]+@([\w-]+\.)+[\w-]{2,4}$"

    user = None

    if re.match(pattern, data):
        user = await Users.get(db, email=data)
    else:
        user = await Users.get(db, username=data)

    return user


async def send_verify_mail(email):
    try:
        message = MessageSchema(
            subject="Subject",
            recipients=[email],
            body="Body",
            subtype=MessageType.html
        )

        fm = FastMail(conf)

        result = await fm.send_message(message=message)

        if result is None:
            return True
        return True
    except:
        raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Server error"
                )

LOGIN_LIMIT_PER_USER = 10
LOGIN_WINDOW_PER_USER = 600

async def login_user_service(
        login: str,
        password: str,
        response: Response,
        db: AsyncSession,
        redis: Redis,
        request: Request
):
    login = str(login).strip()
    password = str(password).strip()

    key = login_key(login)
    login_attempts, ttl = await rate_limit_hit(redis, key, LOGIN_WINDOW_PER_USER)
    if login_attempts > LOGIN_LIMIT_PER_USER:
        raise RateLimitExceeded(message="Many login attemptions", retry_after=ttl)

    existing_user = await auth_by_username_or_email(db, login)
    password_hash = existing_user.password_hash if existing_user else DUMMY_HASH
    check_password = await run_in_threadpool(verify_password, password, password_hash)
    if existing_user is None or not check_password:
        raise InvalidDataForLoginException("Неправильные логин или пароль")

    try:
        await redis.delete(key)
    except:
        raise ServerBadGetwayException("Redis error!")

    old_session_id = request.cookies.get("session_id") 
    if old_session_id:
        await redis.delete(f"session:{old_session_id}")

    session_date = {
        "user_id": str(existing_user.id),
    }

    await create_session(
        str(existing_user.id), 
        session_date,
        response,
        redis
        )

    return existing_user


async def register_user_service(
        username: str,
        email: str,
        password: str,
        db: AsyncSession,
):
    username = str(username).strip()
    email = str(email).strip()
    password = str(password).strip()

    existing_user_by_username = await Users.get(db, username=username)
    existing_user_by_email = await Users.get(db, email=email)

    if existing_user_by_username:
        raise UserAlreadyExistsException("Пользователь с даным username уже зарегистрирован")

    if existing_user_by_email:
        raise UserAlreadyExistsException("Пользователь с данным email уже зарегистрирован")

    try:
        new_user = await Users.put(db, username=username, email=email, password_hash=hash_password(password))
    except IntegrityError:
        await db.rollback()
        raise UserAlreadyExistsException("Пользователь уже зарегистрирован")

    except:
        raise ServiceException("Ошибка в работе сервера")

    return new_user


async def logout_user_server(
    request: Request,
    response: Response,
    redis: Redis,
):
    session_id = request.cookies.get("session_id") 
    
    if session_id:
        await redis.delete(f"session:{session_id}")

    response.delete_cookie(
        key="session_id",
        path="/",
        httponly=True,
        secure=not DEBUG,
        samesite="lax",
    )

    return {"message": "Logged out successfully"}