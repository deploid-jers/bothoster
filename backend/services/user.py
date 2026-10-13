import os, re, json
from fastapi_mail import FastMail, MessageSchema, MessageType
from fastapi import HTTPException, status, Response, Request, BackgroundTasks
from starlette.concurrency import run_in_threadpool
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from redis.asyncio import Redis
from redis.exceptions import RedisError

from database.models.users import Users
from settings.setting import conf

from api.dependencies import get_current_user, rate_limit_hit
from utils.email import confim_email_token, send_verification_email
from core.exceptions import *
from schemas.auth import *
from database.models.users import Users
from core.security import hash_password, verify_password, DUMMY_HASH
from core.sessions import generate_session, create_session, get_session_from_req, destroy_all_sessions, destroy_session
from settings.setting import SESSION_TTL, DEBUG, VERIFY_EMAIL_TTL


from middleware.middleware import logger




async def verify_email_user_service(user: Users, redis: Redis, background_tasks: BackgroundTasks): # TODO Сделать на подтверждение Rate limit
    
    token = confim_email_token() # TODO Сделать sha256 для токена

    try: 
        key = f"verify_email:{token}"
        await redis.set(key, str(user.id), VERIFY_EMAIL_TTL) # TODO Сделать проверку на уже подтверждуную почту
        
        background_tasks.add_task(send_verification_email, user.email, token)

    except RedisError:
        raise ServerBadGetwayException("Redis error!")

    except Exception as e:
        raise ServerErrorException(str(e))


async def confim_email_user_service(token: str, db: AsyncSession, redis: Redis):
    
    try: 
         # TODO Сделать на подтверждение Rate limit
    
        user_id = await redis.getdel(f"verify_email:{token}")
        result = await db.execute(select(Users).where(Users.id == user_id))
        user = result.scalar_one_or_none()

        if user is None:
            raise NotFoundException("Token is invalid!")

        user.is_verified = True
        await db.commit()

        return {"message": "Successfully"}


    except RedisError:
        raise ServerBadGetwayException("Redis error!")

    except Exception as e:
        logger.exception(
            "Unhandled error | exception=%s", # TODO Сделать логирование нормальное
            str(e)
        )



    