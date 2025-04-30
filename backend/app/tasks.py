from celery import Celery
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
import os

celery_app = Celery(
    "tasks",
    broker=os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0"),
)

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("mymail"),
    MAIL_PASSWORD=os.getenv("google_password"),
    MAIL_FROM=os.getenv("mymail"),
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
)


@celery_app.task
def send_verification_email(email: str, token: str, link: str):
    message = MessageSchema(
        subject="Verify Your Email",
        recipients=[email],
        body=f"Click the link to verify your email: {link}",
        subtype="html",
    )
    fm = FastMail(conf)
    import asyncio

    asyncio.run(fm.send_message(message))
