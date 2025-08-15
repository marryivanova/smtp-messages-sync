from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi import APIRouter, Depends, HTTPException, status

from src.config.models import UserDiscounts, Sale
from src.db.database import get_async_session
from src.utils.custom_logger import get_logger


logger = get_logger(__name__)
logger.propagate = False


router_discount = APIRouter(prefix="/discount", tags=["Discount"])


@router_discount.post(
    "/",
    response_model=UserDiscounts,
    status_code=status.HTTP_201_CREATED,
)
async def create_discount(
    discount_data: UserDiscounts,
    session: AsyncSession = Depends(get_async_session),
):
    try:
        new_discount = UserDiscounts(
            user_id=discount_data.user_id,
            promo_code=discount_data.promo_code,
            sale_id=discount_data.sale_id,
        )

        session.add(new_discount)
        await session.commit()
        await session.refresh(new_discount)

        return new_discount

    except IntegrityError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Discount constraint violation (possibly duplicate data)",
        )

    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database operation failed",
        )


@router_discount.post(
    "/{sale_id}",
    response_model=Sale,
    status_code=status.HTTP_201_CREATED,
)
async def create_sale(
    sale_data: Sale,
    session: AsyncSession = Depends(get_async_session),
):
    try:
        new_sale = Sale(
            sale_id=sale_data.sale_id, sale_description=sale_data.sale_description
        )

        session.add(new_sale)
        await session.commit()
        await session.refresh(new_sale)

        return new_sale
    except IntegrityError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Discount constraint violation (possibly duplicate data)",
        )
    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database operation failed",
        )
