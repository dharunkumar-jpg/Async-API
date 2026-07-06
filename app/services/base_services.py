from sqlalchemy.ext.asyncio import AsyncSession

class BaseService:
    """
    Base service responsible for transaction management.
    """

    def __init__(self,session: AsyncSession,) -> None:
        self.session = session

    async def commit(self) -> None:
        """
        Commit the current transaction.
        """
        await self.session.commit()

    async def rollback(self) -> None:
        """
        Roll back the current transaction.
        """
        await self.session.rollback()