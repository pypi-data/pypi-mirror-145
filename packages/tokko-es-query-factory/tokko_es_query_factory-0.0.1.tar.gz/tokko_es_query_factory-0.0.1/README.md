# tokko_es_query_factory
* version: Alfa
* version tag 0.0.1

Cree consultas de ElasticSearch fácilmente

## Install
`
pip install tokko_es_query_factory
`

## Use
```
from tokko_es_query_factory import filters
from tokko_es_query_factory.query_factory import QueryFactory


class FilterFactory(QueryFactory):
    """" Filter Factory! """
    CONFIG = {
        "address": filters.ContainsTextFilter,
        "age": filters.RangeIntFilter
        }
```

## Filter types

* ComplexFilter
* AvailabilityFilter
* MultipleFilter
* OperationFilter
* NetworkFilter
* LocationFilter
* MultipleIntFilter
* MultipleMatch
* MultipleNoMatch
* PositiveIntFilter
* BooleanFilter
* StrFilter
* ContainsTextFilter
* RangeIntFilter
* RangeFloatFilter
* ChoiceIntFilter
* StatusFilter
* DispositionFilter
* CurrencyFilter
* PropertyConditionFilter
* PropertySituationFilter

