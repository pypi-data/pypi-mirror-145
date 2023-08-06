from abc import ABCMeta
from operator import methodcaller
from typing import Any

from sqlalchemy import Column
from sqlalchemy.sql.elements import UnaryExpression

from .alias import AliasedTableMap
from .exc import ApiTypeError
from .pointer import ApiPointer

__all__ = [
    'ApiOrderByDirection',
]


class ApiOrderByDirection(metaclass=ABCMeta):
    __slots__ = '_asc', '_sa_column'

    def __init__(self, sa_column: Column, asc: bool) -> None:
        self._asc = bool(asc)
        self._sa_column = sa_column

    @property
    def sa_column(self) -> Column:
        return self._sa_column

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} ' \
               f'({self.sa_column!r} BY {str(self)})>'

    def __str__(self) -> str:
        return 'ASC' if self._asc else 'DESC'

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            raise ApiTypeError(
                f'Comparison with object of type {self.__class__.__name__!r} '
                f'only is allowed.',
            )
        return str(other) == str(self) and other.sa_column == self.sa_column

    def compile(
        self,
        api_pointer: ApiPointer,
        aliased_table_map: AliasedTableMap,
    ) -> UnaryExpression:
        """Sqlalchemy unary expression for sorting by column."""

        if api_pointer.parent is None:
            column = self.sa_column

        else:
            aliased_table = aliased_table_map[api_pointer]
            column = aliased_table.columns[self.sa_column.key]

        return methodcaller(self._asc and 'asc' or 'desc')(
            column,
        )
