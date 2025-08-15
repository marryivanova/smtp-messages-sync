from fastapi import Query
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status

from src.config.models import (
    UserResponse,
    UserCreate,
    UserUpdate,
)
from src.db.database import get_async_session
from src.db.models import User
from src.utils.custom_logger import get_logger

logger = get_logger(__name__)
logger.propagate = False

router_users = APIRouter(prefix="/user", tags=["User"])

@router_users.get(
    "/", response_model=list[UserResponse], status_code=status.HTTP_200_OK
)
async def get_list_user(
        skip: int = Query(0, ge=0),
        limit: int = Query(20, le=20),
        session: AsyncSession = Depends(get_async_session)
):
    try:
        result = await session.execute(
            select(User).offset(skip).limit(limit)
        )
        users = result.scalars().all()

        return users

    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )

@router_users.post(
    "/", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def create_user(
    user_data: UserCreate, session: AsyncSession = Depends(get_async_session)
):
    try:
        new_user = User(name=user_data.name, email=user_data.email)

        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)

        return new_user

    except Exception as e:
        await session.rollback()
        if "unique constraint" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this name or email already exists",
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router_users.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        user = await session.get(User, user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        await session.delete(user)
        await session.commit()

        return None

    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router_users.patch("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_user(
    user_id: int,
    update_data: UserUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    for field, value in update_data.dict(exclude_unset=True).items():
        setattr(user, field, value)

    try:
        await session.commit()
    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Database error, possibly duplicate email",
        )