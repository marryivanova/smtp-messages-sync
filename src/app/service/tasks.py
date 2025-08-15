import typing as t
from sqlalchemy import select
from sqlalchemy.orm import Session
from src.app.service.celery_app import app
from src.app.service.smtp_email import SmtpEmailBackend
from src.config.settings import settings
from src.db.models import User
from src.helpers.template_message import create_email
from src.utils.custom_logger import get_logger

logger = get_logger(__name__)
logger.propagate = False


def fetch_users_info(session: Session, user_ids: t.List[int]) -> t.List[t.Tuple[str, str]]:
    """Fetch user information based on their IDs."""
    result = session.execute(
        select(User).where(User.id.in_(user_ids)))
    users = result.scalars().all()
    return [(user.name, user.email) for user in users]


@app.task(bind=True, max_retries=3)
def send_email_newsletter(
        self,
        user_ids: t.List[int],
        promo_code: str,
        sale_id: int,
        discount: int,
) -> None:
    """Send newsletter emails to multiple users."""
    logger.info(
        "Starting newsletter #%s email campaign for %s users",
        sale_id,
        len(user_ids),
    )

    if not user_ids:
        logger.warning("No users to send newsletter #%s", sale_id)
        return

    try:
        email_backend = SmtpEmailBackend(
            smtp_server=settings.SMTP_SERVER,
            smtp_port=settings.SMTP_PORT,
            from_email=settings.FROM_EMAIL,
        )

        with Session() as session:
            users_info = fetch_users_info(session, user_ids)

            if not users_info:
                logger.warning("No users found for newsletter #%s", sale_id)
                return

            total_sent = 0
            total_users = len(users_info)

            for name, email in users_info:
                try:
                    subject = f"{name}, join our sale #{sale_id}!"
                    body = create_email(
                        name=name,
                        sale_id=sale_id,
                        promo=promo_code,
                        discount=discount,
                    )

                    email_backend.send_email(
                        recipient=email,
                        subject=subject,
                        body=body,
                    )
                    total_sent += 1
                    logger.info("Successfully sent email to %s", email)

                except Exception as e:
                    logger.error(
                        "Failed to send email to %s: %s", email, str(e), exc_info=True
                    )
                    continue

            logger.info(
                "Completed newsletter #%s: Successfully sent %s/%s emails",
                sale_id,
                total_sent,
                total_users,
            )

    except Exception as e:
        logger.error(
            "Failed to process newsletter #%s: %s", sale_id, str(e), exc_info=True
        )
        self.retry(exc=e, countdown=60)