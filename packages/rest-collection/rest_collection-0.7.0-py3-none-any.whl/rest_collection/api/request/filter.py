from rest_collection.container import Aliases
from ..abc import AbstractApiFilterRequestContext
from ..exc import ApiFilterError
from ..param import ApiContextParamSchema, ApiContextParamSchemaNode, \
    ApiContextParams, ApiParam

__all__ = [
    'ApiFilterRequestContext',
]


def _nomalize_filter(url_param: ApiParam) -> str:
    try:
        return url_param.value.strip()
    except AttributeError as err:
        raise ApiFilterError() from err


class ApiFilterRequestContext(AbstractApiFilterRequestContext):
    __slots__ = ()

    URL_PARAM_SCHEMA = ApiContextParamSchema(
        ApiContextParamSchemaNode(Aliases('filter'), _nomalize_filter),
    )

    def _initialize(self) -> None:
        url_param_schema = self.__class__.URL_PARAM_SCHEMA
        context_url_params = ApiContextParams(self.request, url_param_schema)

        filter_url_param = context_url_params.get_first(
            url_param_schema.main_for('filter'),
        )

        self._data = self._parser.parse(
            getattr(filter_url_param, 'value', None),
        )
