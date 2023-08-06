from abc import abstractmethod
from typing import Iterator, Mapping

from rest_collection.container import WeakKeyOrderedDict
from .request import AbstractApiRequest, AbstractApiRequestContext
from ..order_by import ApiOrderByDirection
from ..pointer import ApiPointer

__all__ = [
    'AbstractApiOrderByRequestContext',
]


class AbstractApiOrderByRequestContext(
    AbstractApiRequestContext,
    Mapping[ApiPointer, ApiOrderByDirection],
):

    __slots__ = ('_data',)

    def __init__(self, request: AbstractApiRequest) -> None:
        self._data = WeakKeyOrderedDict()
        super().__init__(request)

    @abstractmethod
    def _initialize(self) -> None: ...

    def __getitem__(self, key: ApiPointer) -> ApiOrderByDirection:
        return self._data[key]

    def __iter__(self) -> Iterator[ApiPointer]:
        return iter(self._data)

    def __len__(self) -> int:
        return len(self._data)

    def __repr__(self) -> str:
        order_clauses = ', '.join(
            f'{k!r}={"asc" if bool(v) else "desc"}'
            for k, v in self._data.items()
        )
        return f'<{self.__class__.__name__} ({order_clauses})>'

    def __bool__(self) -> bool:
        return len(self._data) > 0
