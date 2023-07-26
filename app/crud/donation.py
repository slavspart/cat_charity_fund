from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase, get_diff_or_zero
from app.models import CharityProject, Donation


class CRUDDonation(CRUDBase):
    async def invest_donation(
        self,
        donation: Donation,
        session: AsyncSession,
    ) -> None:
        fnc = await session.execute(
            select(CharityProject)
            .where(CharityProject.full_amount > 0)
            .order_by(CharityProject.create_date)
        )
        fnc = fnc.scalars().all()
        if fnc is not None:
            for project in fnc:
                while (
                    donation.full_amount > donation.invested_amount and
                    project.full_amount > project.invested_amount
                ):
                    print(
                        "d",
                        donation.invested_amount,
                        "p",
                        project.invested_amount,
                        project,
                    )
                    to_invest = project.full_amount - project.invested_amount
                    money = donation.full_amount - donation.invested_amount
                    project.invested_amount += to_invest - get_diff_or_zero(
                        to_invest, money
                    )
                    donation.invested_amount += money - get_diff_or_zero(
                        money, to_invest
                    )
                    print(
                        "d",
                        donation.invested_amount,
                        "p",
                        project.invested_amount,
                        project,
                    )
                    donation.close()
                    project.close()
            await session.commit()
            await session.refresh(donation)


donation_crud = CRUDDonation(Donation)
