from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks

from src.app.service.smtp_email import SmtpEmailBackend
from src.config.models import (
    UserResponse,
    UserCreate,
    UserUpdate,
    UserDiscounts,
    EmailRequest, Sale,
)
from src.db.database import get_async_session
from src.db.models import User
from src.utils.custom_logger import get_logger


logger = get_logger(__name__)
logger.propagate = False

router = APIRouter(prefix="/smtp", tags=["SMTP message"])


# @router.post("/send-email")
# async def send_message(
#     request: EmailRequest,
#     background_tasks: BackgroundTasks,
#     email_backend: SmtpEmailBackend,
# ):
#     background_tasks.add_task(
#         email_backend.send_email,
#         recipient=request.recipient,
#         subject=request.subject,
#         body=request.body,
#     )
#     return {"status": "Email queued for sending"}


