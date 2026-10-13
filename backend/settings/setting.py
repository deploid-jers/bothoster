import os
from pathlib import Path
from dotenv import load_dotenv
from fastapi_mail import ConnectionConfig

from settings.pathes import BASE_DIR



load_dotenv(str(BASE_DIR / ".env"))



DEBUG = bool(os.getenv("DEBUG")) or True
DATABASE_URL = os.getenv("DATABASE_URL")

DOMAIN_NAME = os.getenv("DOMAIN_NAME") or "myproject"
HOST = os.getenv("HOST") or "0.0.0.0"
PORT = int(os.getenv("PORT")) or 8000

FRONTEND_HOST = os.getenv("FRONTEND_HOST")
FRONTEND_PORT = os.getenv("FRONTEND_PORT")
FRONTEND_URL = f"http://{FRONTEND_HOST}:{FRONTEND_PORT}"


SESSION_TTL = 60 * 60
VERIFY_EMAIL_TTL = 60 * 5

# ==== REDIS
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv('REDIS_PORT'))
# ====

ALLOWED_ORIGINS = [
    f"https://{DOMAIN_NAME}.com",
    f"https://admin.{DOMAIN_NAME}.com",
]

ALLOWED_HOSTS = [
    f"{DOMAIN_NAME}.com",
    f"admin.{DOMAIN_NAME}.com",
    f"api.{DOMAIN_NAME}.com"
]


# ========= Конфиг для Email рассылки =====
conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=os.getenv("MAIL_PORT"),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_SSL_TLS=os.getenv("MAIL_SSL_TLS"),    
    MAIL_STARTTLS=os.getenv("MAIL_STARTTLS"), 
    USE_CREDENTIALS=os.getenv("USE_CREDENTIALS"),
    VALIDATE_CERTS=os.getenv("VALIDATE_CERTS")
)