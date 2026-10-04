from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn

from settings.setting import DEBUG, HOST, PORT, DOMAIN_NAME
from middleware.middleware import setup_middleware

from api.router import router as api_router

from redis_client.redis_client import init_redis_pool, close_resis_pool, check_connection
from database.first_init import first_init

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_redis_pool()
    await check_connection()
    print("Redis подключение инициализировано")
    await first_init()

    print(f"Сервер доступен по адресу: http://{DOMAIN_NAME}:{PORT} или http://{HOST}:{PORT}")

    yield

    await close_resis_pool()
    print("Redis подключение закрыто")



app = FastAPI(
    title="BotHoster - Платформа для хостинга ботов",
    debug=DEBUG,
    docs_url='/docs' if DEBUG else None,
    redoc_url='/redoc' if DEBUG else None,
    lifespan=lifespan,
    )

setup_middleware(app) 

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(api_router)



if __name__ == "__main__":
    uvicorn.run(app="main:app", host=HOST, port=PORT, reload=True)

