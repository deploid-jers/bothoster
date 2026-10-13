import secrets
import logging
from html import escape
from urllib.parse import quote
from settings.pathes import BASE_DIR
from settings.setting import conf, FRONTEND_URL
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType


logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(f"{str(BASE_DIR)}/logging/email.log", encoding="utf-8")
    ]
)

def confim_email_token() -> str:
    token = secrets.token_urlsafe(32)
    return token


def render_template_verification_email(token: str) -> str:
    link = f"{FRONTEND_URL}/verify?token={quote(token, safe='')}"
    link_html = escape(link)

    return f"""\
<!DOCTYPE html>
<html lang="ru">
<body style="margin:0;padding:0;background:#f4f5f7;font-family:Arial,Helvetica,sans-serif;">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#f4f5f7;padding:32px 0;">
    <tr><td align="center">
      <table role="presentation" width="560" cellpadding="0" cellspacing="0"
             style="max-width:560px;width:100%;background:#ffffff;border-radius:12px;">
        <tr><td style="padding:32px 32px 8px 32px;font-size:22px;font-weight:bold;color:#1a1d24;">
          Подтвердите ваш email
        </td></tr>
        <tr><td style="padding:8px 32px;font-size:15px;line-height:1.6;color:#4a4f5a;">
          Вы зарегистрировались в MyApp. Нажмите кнопку ниже, чтобы активировать аккаунт.
          Ссылка действует 24 часа и сработает один раз.
        </td></tr>
        <tr><td align="center" style="padding:24px 32px;">
          <a href="{link_html}"
             style="display:inline-block;background:#6c8cff;color:#ffffff;text-decoration:none;
                    padding:14px 28px;border-radius:8px;font-size:16px;font-weight:bold;">
            Подтвердить email
          </a>
        </td></tr>
        <tr><td style="padding:0 32px 8px 32px;font-size:13px;color:#7a808c;">
          Если кнопка не работает, скопируйте ссылку в браузер:
        </td></tr>
        <tr><td style="padding:0 32px 24px 32px;font-size:13px;word-break:break-all;">
          <a href="{link_html}" style="color:#6c8cff;">{link_html}</a>
        </td></tr>
        <tr><td style="padding:16px 32px 32px 32px;border-top:1px solid #eceef2;font-size:12px;color:#9aa0a6;">
          Если это были не вы, просто проигнорируйте письмо: без подтверждения ничего не произойдёт.
        </td></tr>
      </table>
    </td></tr>
  </table>
</body>
</html>"""


async def send_verification_email(email, token):
    try:
        html = render_template_verification_email(token)
        message = MessageSchema(
            subject="Fastapi-Mail module",
            recipients=[str(email)],
            body=html,
            subtype=MessageType.html
        )

        fm = FastMail(conf)
        await fm.send_message(message)
        logging.info("Mail sended | email=%s", email)

    except Exception as e:
        logging.exception(
            "Unhandled error | verify_email=%s | message=%s",
            email,
            str(e)
        )