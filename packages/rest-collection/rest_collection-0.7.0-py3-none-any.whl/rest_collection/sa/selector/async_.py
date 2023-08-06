from typing import List, Optional

from sqlalchemy import func, select
from sqlalchemy.engine import Result
from sqlalchemy.engine.row import Row
from sqlalchemy.ext.asyncio import AsyncEngine

from .abc import AbstractAsyncSqlalchemySelector
from .mixin import SqlalchemySelectorMixin

__all__ = [
    'AsyncSqlalchemySelector',
]


class AsyncSqlalchemySelector(
    SqlalchemySelectorMixin,
    AbstractAsyncSqlalchemySelector[AsyncEngine],
):
    """Async selector."""
    __slots__ = ()

    async def select(self, *args, **kwargs) -> List[Row]:
        sa_query = self.get_query()

        async with self._sa_engine.connect() as conn:
            result: Result = await conn.execute(sa_query)
            return result.fetchall()

    async def count(self, *args, **kwargs) -> Optional[int]:
        sa_query = self.get_query(for_counting=True)
        sa_query = select(func.count()).select_from(sa_query.alias())

        async with self._sa_engine.connect() as conn:
            result: Result = await conn.execute(sa_query)
            return result.scalar()
