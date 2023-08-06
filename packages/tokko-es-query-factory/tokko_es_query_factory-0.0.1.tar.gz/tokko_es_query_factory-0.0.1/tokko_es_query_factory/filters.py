import datetime
import json
from abc import ABC
from dataclasses import dataclass, field
from typing import Dict, Any, List

from elasticsearch_dsl import Q
from elasticsearch_dsl.query import Bool

from .exceptions import InputError, EmptyInput


@dataclass(init=True)
class BaseFilter(ABC):
    field_name: str
    value: Any

    def __post_init__(self):
        self.validate()

    def validate(self):
        raise NotImplementedError

    def get_query(self) -> Q:
        return Q("match", **{self.field_name: self.value})


@dataclass(init=True)
class ComplexFilter(BaseFilter):
    def validate(self):
        try:
            self.value = json.loads(self.value)
        except (json.decoder.JSONDecodeError, TypeError):
            ...
        if not type(self.value) == bool and not self.value:
            raise EmptyInput


@dataclass(init=True)
class AvailabilityFilter(ComplexFilter):
    def validate(self):
        super().validate()
        try:
            date_from = self.value["date_from"]
            date_to = self.value["date_to"]
            _format = "%Y-%m-%d"
            datetime.datetime.strptime(date_from, _format)
            datetime.datetime.strptime(date_to, _format)
        except (ValueError, KeyError, TypeError):
            raise InputError

    def get_query(self) -> Q:
        query = (
            Q("range", **{"availability__date_from": {"lte": self.value["date_to"]}}) +
            Q("range", **{"availability__date_to": {"gte": self.value["date_from"]}})
        )
        return ~Q("nested", path="availability", query=query)


@dataclass(init=False)
class MultipleFilter(ComplexFilter):
    config: Dict = None
    filters: Dict = None

    def validate(self):
        super().validate()
        if not type(self.value) == dict:
            raise InputError(f'Invalid input: {str(self.value)}')

    def fill_filters(self):
        for _field, _config in self.config.items():
            val = self.value.get(_field)
            try:
                self.filters.update({_field: _config["filter"](_config["el_field"], val)})
            except (EmptyInput, InputError):
                ...

    def __post_init__(self):
        super().__post_init__()
        self.fill_filters()


class OperationFilter(MultipleFilter):
    def __init__(self, *args):
        self.config = {
            "operation_type": {"el_field": "operations__operation_type", "filter": MultipleIntFilter},
            "prices": {"el_field": "operations__prices__price", "filter": RangeFloatFilter},
        }
        self.filters = {}
        super().__init__(*args)

    def get_query(self) -> Q:
        query = None
        for k, v in self.filters.items():
            if query:
                query = query + self.filters[k].get_query()
            else:
                query = self.filters[k].get_query()
        if query:
            return Q("nested", path="operations", query=query)
        else:
            raise EmptyInput


class NetworkFilter(MultipleFilter):
    def __init__(self, *args):
        self.config = {
            "network_id": {"el_field": "networkinfo__network_id", "filter": PositiveIntFilter},
            "share": {"el_field": "networkinfo__share", "filter": BooleanFilter},
        }
        self.filters = {}
        super().__init__(*args)

    def get_query(self) -> Q:
        query = None
        for k, v in self.filters.items():
            if query:
                query = query + self.filters[k].get_query()
            else:
                query = self.filters[k].get_query()
        if query:
            return Q("nested", path="networkinfo", query=query)
        else:
            raise EmptyInput


class LocationFilter(MultipleFilter):
    def __init__(self, *args):
        self.config = {
            "divisions": {"el_field": "location__id", "filter": MultipleIntFilter},
            "states": {"el_field": "location__state", "filter": MultipleIntFilter},
            "countries": {"el_field": "location__country", "filter": MultipleIntFilter},
        }
        self.filters = {}
        super().__init__(*args)

    def get_query(self) -> Q:
        query = None
        for k, v in self.filters.items():
            if query:
                query = query | self.filters[k].get_query()
            else:
                query = self.filters[k].get_query()
        if query:
            return query
        else:
            raise EmptyInput


@dataclass(init=True)
class MultipleIntFilter(ComplexFilter):
    value: List[int]

    def validate(self):
        super().validate()
        if any([
            not type(self.value) == list
        ]) or not all(type(i) == int and i >= 0 for i in self.value):
            raise InputError(f'Invalid input: {str(self.value)}')


    def get_query(self) -> Q:
        if self.value[0] > 0:
            query = Q("match", **{self.field_name: self.value[0]})
        elif self.value[0] == 0:
            query = ~Q("exists", **{"field": self.field_name})

        for i in self.value[1:]:
            if i > 0:
                query = query | Q("match", **{self.field_name: i})
            elif i == 0:
                query = query | ~Q("exists", **{"field": self.field_name})
        return Bool(must=[query])


class MultipleMatch(MultipleIntFilter):

    def get_query(self) -> Q:
        field = self.field_name.split("_", 1)[1]
        query = Q("match", **{field: self.value[0]})
        for i in self.value[1:]:
            query = query + Q("match", **{field: i})
        return query


class MultipleNoMatch(MultipleIntFilter):
    def get_query(self) -> Q:
        field = self.field_name.split("_", 1)[1]
        query = ~Q("match", **{field: self.value[0]})
        for i in self.value[1:]:
            query = query | ~Q("match", **{field: i})
        return query


@dataclass(init=True)
class PositiveIntFilter(BaseFilter):
    value: int

    def validate(self):
        try:
            self.value = int(self.value)
            if self.value < 0:
                raise ValueError
        except (ValueError, TypeError):
            raise InputError(f'Invalid input {str(self.value)}')

    def get_query(self) -> Q:
        if self.value > 0:
            return Q("match", **{self.field_name: self.value})
        else:
            return ~Q("exists", **{"field": self.field_name})


@dataclass(init=True)
class BooleanFilter(ComplexFilter):
    value: bool

    def validate(self):
        super().validate()
        if not type(self.value) == bool:
            raise InputError(f'Invalid input: {str(self.value)}')


@dataclass(init=True)
class StrFilter(BaseFilter):
    value: str
    rules: List[str] = field(default_factory=list)

    def validate(self):
        if self.rules and self.value not in self.rules:
            raise InputError(f'Invalid input {self.value}')


@dataclass(init=True)
class ContainsTextFilter(ComplexFilter):
    value: dict

    def validate(self):
        super().validate()
        if (
            not type(self.value) == dict or
            "contains" not in self.value or
            "text" not in self.value
        ):
            raise InputError(f'Invalid input: {str(self.value)}')


    def get_query(self) -> Q:
        text = self.value.get("text", "")
        query = f"*{text}*"
        contains = self.value.get("contains", True)
        if contains:
            return Q("wildcard", **{self.field_name.replace("__", "."): {"value": query}})
        else:
            return ~Q("wildcard", **{self.field_name.replace("__", "."): {"value": query}})


class RangeIntFilter(ComplexFilter):

    value: dict

    def validate(self):
        super().validate()

        VALID_KEYS = ["gte", "gt", "lt", "lte"]

        if any([
            not type(self.value) == dict
        ]) or not all(x in VALID_KEYS and type(y) == int for x, y in self.value.items()):
            raise InputError(f'Invalid input: {str(self.value)}')

    def get_query(self) -> Q:
        return Q("range", **{self.field_name: self.value})


class RangeFloatFilter(ComplexFilter):
    value: dict

    def validate(self):
        super().validate()

        VALID_KEYS = ["gte", "gt", "lt", "lte"]

        if any([
            not type(self.value) == dict
        ]) or not all(x in VALID_KEYS and type(y) == int or type(y) == float for x, y in self.value.items()):
            raise InputError(f'Invalid input: {str(self.value)}')

    def get_query(self) -> Q:
        return Q("range", **{self.field_name: self.value})


@dataclass(init=True)
class ChoiceIntFilter(BaseFilter):
    rules: List[int]

    def validate(self):
        try:
            self.value = int(self.value)
            if self.value not in self.rules:
                raise ValueError
        except (ValueError, TypeError):
            raise InputError(f'Invalid input {str(self.value)}')


class StatusFilter(ChoiceIntFilter):

    def __init__(self, *args):
        rules = [1, 2, 3, 4]
        super().__init__(*args, **{"rules": rules})


class DispositionFilter(ChoiceIntFilter):
    def __init__(self, *args):
        rules = [0, 1, 2, 3, 4]
        super().__init__(*args, **{"rules": rules})


class CurrencyFilter(StrFilter):
    def __init__(self, *args):
        self.rules = ["ARS", "USD"]
        super().__init__(*args)

    def validate(self):
        self.value = self.value.upper()
        super().validate()


class PropertyConditionFilter(StrFilter):
    def __init__(self, *args):
        self.rules = ["---", "To refurbish", "Good", "Excellent", "Very good", "Recicled", "Regular"]
        super().__init__(*args)


class PropertySituationFilter(StrFilter):
    def __init__(self, *args):
        self.rules = ["---", "In use", "Empty"]
        super().__init__(*args)
