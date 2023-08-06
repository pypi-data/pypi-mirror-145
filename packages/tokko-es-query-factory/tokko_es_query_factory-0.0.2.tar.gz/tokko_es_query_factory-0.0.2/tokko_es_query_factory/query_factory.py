from abc import ABC
from dataclasses import dataclass
from typing import Dict, List

from elasticsearch_dsl import Q

from .exceptions import InputError, InvalidFilters, EmptyInput


@dataclass(init=True)
class QueryFactory(ABC):
    """" Filter Factory! """
    CONFIG = dict()
    filters: [dict]

    def __post_init__(self):
        errors = []
        for i in self.filters.keys():
            if i not in self.CONFIG.keys():
                errors.append(i)
        if errors:
            raise InvalidFilters(errors)

    def build(self) -> (List[Q], List[Dict]):
        errors = {}
        filters = Q()
        for _field, value in self.filters.items():
            try:
                if value:
                    filters = filters + self.CONFIG[_field](_field, value).get_query()
            except InputError:
                errors.update({_field: value})
            except EmptyInput:
                ...
        return filters, errors
