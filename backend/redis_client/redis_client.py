from typing import AsyncGenerator
import redis.asyncio as aioredis

from settings.setting import REDIS_HOST, REDIS_PORT

redis_client: aioredis.Redis | None = None


async def init_redis_pool() -> None:
    """Инициализация подключения к Redis"""
    global redis_client
    redis_client = aioredis.from_url(
        f"redis://{REDIS_HOST}:{REDIS_PORT}/0",
        encoding="utf-8",
        decode_responses=True
    )



async def check_connection() -> None:
    """Проверка подлкючения к Redis"""
    try:
        global redis_client

        async with redis_client:
            if not await redis_client.ping():
                raise RuntimeError("Ошибка подключения")

    except aioredis.AuthenticationError:
        raise RuntimeError(" Ошибка: Неверный пароль (AuthenticationError).")
        
    except aioredis.ConnectionError as e:
        raise RuntimeError(f" Ошибка подключения: Redis недоступен.\nДетали: {e}")
        
    except Exception as e:
        raise RuntimeError(f" Произошла непредвиденная ошибка: {e}")



async def close_resis_pool() -> None:
    global redis_client
    if redis_client is not None:
        await redis_client.close()

async def get_redis() -> AsyncGenerator[aioredis.Redis, None]:
    """Внедрение зависимости для эндпоинтов"""
    if redis_client is None:
        raise RuntimeError("Клиент Redis не инициализирован!")
    yield redis_client