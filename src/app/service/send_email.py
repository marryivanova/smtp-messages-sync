import random
import string
import typing as t

from sqlalchemy import select

from src.app.service.tasks import send_email_newsletter
from src.db.database import get_async_session
from src.db.models import User
from src.helpers.generate_promo import generate_promo
from src.utils.custom_logger import get_logger

logger = get_logger(__name__)
logger.propagate = False


async def fetch_users_ids_for_newsletter() -> t.List[int]:
    """Fetch active user IDs from database for newsletter sending.

    Returns:
        List of active user IDs.
    """
    async with get_async_session() as session:
        result = await session.execute(select(User.id).where(User.is_active == True))
        return [row[0] for row in result.all()]


async def send_newsletters_task() -> t.Any | None:
    """Prepare and send newsletter emails to all active users.

    Returns:
        Celery AsyncResult for tracking task status.
    """
    try:
        user_ids = await fetch_users_ids_for_newsletter()

        if not user_ids:
            logger.warning("No active users found for newsletter")
            return None

        promo_code = generate_promo()
        sale_id = random.randint(50, 200)

        result = send_email_newsletter.delay(
            user_ids=user_ids,
            promo_code=promo_code,
            sale_id=sale_id,
            discount=15,
        )

        logger.info(
            "Sent newsletter task %s for %d users, sale #%d",
            result.id,
            len(user_ids),
            sale_id,
        )
        return result

    except Exception as e:
        logger.error("Failed to send newsletters task: %s", str(e), exc_info=True)
        raise
