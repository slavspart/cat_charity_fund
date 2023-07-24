from typing import List
from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.donation import donation_crud
from app.schemas.donation import DonationCreate, DonationDB_short, DonationDB_long
from app.core.user import current_user
from app.models import Donation, User

router = APIRouter()


@router.post(
    '/',
    response_model=DonationDB_short,
    response_model_exclude_none=True,
)
async def create_new_donation(
        donation: DonationCreate,
        # schema
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):

    new_donation = await donation_crud.create(donation, session, user)
    await donation_crud.invest_donation(new_donation, session)
    return new_donation


@router.get(
    '/',
    response_model=List[DonationDB_long],
    response_model_exclude_none=True,
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session),
):
    donations = await donation_crud.get_multi(session)
    return donations


@router.get(
    '/my', response_model=List[DonationDB_short],
)
async def get_my_donations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    """Получает список всех пожертвований для текущего пользователя."""
    donations = await donation_crud.get_by_user(
        Donation, session, user
    )
    return donations
