from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase, get_diff_or_zero
from app.models import CharityProject, Donation


class CRUDCharityProject(CRUDBase):
    async def invest_donation(
        self,
        project: CharityProject,
        session: AsyncSession,
    ) -> None:
        unused_donations = await session.execute(
            select(Donation)
            .where(Donation.full_amount > 0)
            .order_by(Donation.create_date)
        )
        # getting unused donations
        unused_donations = unused_donations.scalars().all()
        if unused_donations is not None:
            for donation in unused_donations:
                while (
                    project.full_amount > project.invested_amount
                    and donation.full_amount > donation.invested_amount
                ):
                    to_invest = project.full_amount - project.invested_amount
                    # amount needed to accomplish project
                    money = donation.full_amount - donation.invested_amount
                    # money left in this donation
                    project.invested_amount += to_invest - get_diff_or_zero(
                        to_invest, money
                    )
                    # increase project invested amount by the money of the donation until it is full
                    donation.invested_amount += money - get_diff_or_zero(
                        money, to_invest
                    )
                    # increase donation invested amount by the summ which is spent
                    donation.close()
                    project.close()
            await session.commit()
            await session.refresh(project)


charity_project_crud = CRUDCharityProject(CharityProject)
