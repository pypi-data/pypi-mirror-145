from itertools import chain
from operator import methodcaller
from typing import Iterator, MutableSequence, Optional, Sequence, Tuple

from sqlalchemy import Column, Table
from sqlalchemy.sql import Alias
from sqlalchemy.sql.elements import Label

from rest_collection.typing import SelectableElementType
from .join import JoinMap

__all__ = [
    'SelectCollection',
    'SelectElement',
]


def _element_is_table(sa_element: SelectableElementType) -> bool:
    return isinstance(sa_element, (Table, Alias))


class SelectElement(Sequence[Column]):
    """Element container, that can be included into select statement."""
    __slots__ = (
        '_sa_element',
        '_label_or_prefix',
        '_data',
        '_is_table',
    )

    def __init__(
        self,
        sa_element: SelectableElementType,
        label_or_prefix: str,
    ) -> None:
        is_table = _element_is_table(sa_element)

        self._sa_element = sa_element
        self._label_or_prefix = label_or_prefix

        self._is_table = is_table

        if is_table:
            self._data = tuple(sa_element.columns)

        else:
            self._data = (sa_element,)

    @property
    def sa_element(self) -> SelectableElementType:
        return self._sa_element

    @property
    def is_table(self) -> bool:
        return self._is_table

    @property
    def is_element(self) -> bool:
        return not self._is_table

    def _label_column(self, column: Column) -> Label:
        # usage as prefix.
        return column.label(f'{self._label_or_prefix}{column.key}')

    def __iter__(self) -> Iterator[Label]:
        if self._is_table:
            return iter(map(self._label_column, self._data))

        return iter(
            map(
                # usage as label.
                methodcaller('label', self._label_or_prefix),
                self._data,
            ),
        )

    def __len__(self) -> int:
        return len(self._data)

    def __getitem__(self, index: int) -> Column:
        return self._data[index]

    @property
    def label(self) -> Optional[str]:
        if not self._is_table:
            return self._label_or_prefix

    @property
    def prefix(self) -> Optional[str]:
        if self._is_table:
            return self._label_or_prefix

    def __repr__(self) -> str:
        return (
            f'<{self.__class__.__name__} '
            f'sa_element={self._sa_element!r} '
            f'label={self.label!r} '
            f'prefix={self.prefix!r} '
            f'data={self._data!r}>'
        )


class SelectCollection(MutableSequence[SelectElement]):
    """Sequence of columns, that will be participate in select part or
    sql statement."""

    __slots__ = '_data', '__weakref__'

    def __init__(self) -> None:
        self._data = []

    def __getitem__(self, index: int) -> SelectElement:
        return self._data[index]

    def insert(self, index: int, value: SelectElement) -> None:
        assert isinstance(value, SelectElement)
        self._data.insert(index, value)

    def __setitem__(self, index: int, value: SelectElement) -> None:
        assert isinstance(value, SelectElement)
        self._data[index] = value

    def __len__(self) -> int:
        return len(self._data)

    def __delitem__(self, index: int) -> None:
        del self._data[index]

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} data={self._data!r}>'

    @property
    def selectable(self) -> Tuple[Label, ...]:
        return tuple(chain.from_iterable(self._data))

    @classmethod
    def from_join_map(
        cls,
        table: Table,
        join_map: JoinMap,
    ) -> 'SelectCollection':
        collection = cls()

        aliased_table_map = join_map.aliased_table_map
        alias_map = aliased_table_map.alias_map

        # Adding primary model of api request.
        collection.append(
            SelectElement(table, ''),
        )

        # Adding other models of api request.
        collection.extend((
            SelectElement(
                aliased_table_map[api_pointer],
                f'{alias_map[api_pointer]}_',
            ) for api_pointer in join_map
        ))

        return collection
