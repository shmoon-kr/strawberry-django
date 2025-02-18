import datetime
import decimal
import uuid
from typing import (
    Generic,
    Optional,
    Union,
    TypeVar,
    Annotated,
    TYPE_CHECKING,
)

import strawberry
from django.core.exceptions import ImproperlyConfigured
from django.db.models import Q
from strawberry import UNSET

from strawberry_django.filters import resolve_value

from .filter_order import filter_field
if TYPE_CHECKING:
    from .types import Geometry

T = TypeVar("T")

_SKIP_MSG = "Filter will be skipped on `null` value"


@strawberry.input
class BaseFilterLookup(Generic[T]):
    exact: Optional[T] = filter_field(description=f"Exact match. {_SKIP_MSG}")
    is_null: Optional[bool] = filter_field(description=f"Assignment test. {_SKIP_MSG}")
    in_list: Optional[list[T]] = filter_field(
        description=f"Exact match of items in a given list. {_SKIP_MSG}"
    )


@strawberry.input
class RangeLookup(Generic[T]):
    start: Optional[T] = None
    end: Optional[T] = None

    @filter_field
    def filter(self, queryset, prefix: str):
        return queryset, Q(**{
            prefix[:-2]: [resolve_value(self.start), resolve_value(self.end)]
        })


@strawberry.input
class ComparisonFilterLookup(BaseFilterLookup[T]):
    gt: Optional[T] = filter_field(description=f"Greater than. {_SKIP_MSG}")
    gte: Optional[T] = filter_field(
        description=f"Greater than or equal to. {_SKIP_MSG}"
    )
    lt: Optional[T] = filter_field(description=f"Less than. {_SKIP_MSG}")
    lte: Optional[T] = filter_field(description=f"Less than or equal to. {_SKIP_MSG}")
    range: Optional[RangeLookup[T]] = filter_field(
        description="Inclusive range test (between)"
    )


@strawberry.input
class FilterLookup(BaseFilterLookup[T]):
    i_exact: Optional[T] = filter_field(
        description=f"Case-insensitive exact match. {_SKIP_MSG}"
    )
    contains: Optional[T] = filter_field(
        description=f"Case-sensitive containment test. {_SKIP_MSG}"
    )
    i_contains: Optional[T] = filter_field(
        description=f"Case-insensitive containment test. {_SKIP_MSG}"
    )
    starts_with: Optional[T] = filter_field(
        description=f"Case-sensitive starts-with. {_SKIP_MSG}"
    )
    i_starts_with: Optional[T] = filter_field(
        description=f"Case-insensitive starts-with. {_SKIP_MSG}"
    )
    ends_with: Optional[T] = filter_field(
        description=f"Case-sensitive ends-with. {_SKIP_MSG}"
    )
    i_ends_with: Optional[T] = filter_field(
        description=f"Case-insensitive ends-with. {_SKIP_MSG}"
    )
    regex: Optional[T] = filter_field(
        description=f"Case-sensitive regular expression match. {_SKIP_MSG}"
    )
    i_regex: Optional[T] = filter_field(
        description=f"Case-insensitive regular expression match. {_SKIP_MSG}"
    )


@strawberry.input
class DateFilterLookup(ComparisonFilterLookup[T]):
    year: Optional[ComparisonFilterLookup[int]] = UNSET
    month: Optional[ComparisonFilterLookup[int]] = UNSET
    day: Optional[ComparisonFilterLookup[int]] = UNSET
    week_day: Optional[ComparisonFilterLookup[int]] = UNSET
    iso_week_day: Optional[ComparisonFilterLookup[int]] = UNSET
    week: Optional[ComparisonFilterLookup[int]] = UNSET
    iso_year: Optional[ComparisonFilterLookup[int]] = UNSET
    quarter: Optional[ComparisonFilterLookup[int]] = UNSET


@strawberry.input
class TimeFilterLookup(ComparisonFilterLookup[T]):
    hour: Optional[ComparisonFilterLookup[int]] = UNSET
    minute: Optional[ComparisonFilterLookup[int]] = UNSET
    second: Optional[ComparisonFilterLookup[int]] = UNSET
    date: Optional[ComparisonFilterLookup[int]] = UNSET
    time: Optional[ComparisonFilterLookup[int]] = UNSET


@strawberry.input
class DatetimeFilterLookup(DateFilterLookup[T], TimeFilterLookup[T]):
    pass


type_filter_map = {
    strawberry.ID: BaseFilterLookup,
    bool: BaseFilterLookup,
    datetime.date: DateFilterLookup,
    datetime.datetime: DatetimeFilterLookup,
    datetime.time: TimeFilterLookup,
    decimal.Decimal: ComparisonFilterLookup,
    float: ComparisonFilterLookup,
    int: ComparisonFilterLookup,
    str: FilterLookup,
    uuid.UUID: FilterLookup,
}


try:
    from django.contrib.gis.geos import GEOSGeometry
except ImproperlyConfigured:
    # If gdal is not available, skip.
    pass
else:
    @strawberry.input
    class GeometryFilterLookup(Generic[T]):
        bbcontains: Optional[Annotated["Geometry", strawberry.lazy(".types")]] = UNSET
        bboverlaps: Optional[Annotated["Geometry", strawberry.lazy(".types")]] = UNSET
        contained: Optional[Annotated["Geometry", strawberry.lazy(".types")]] = UNSET
        contains: Optional[Annotated["Geometry", strawberry.lazy(".types")]] = UNSET
        contains_properly: Optional[Annotated["Geometry", strawberry.lazy(".types")]] = UNSET
        coveredby: Optional[Annotated["Geometry", strawberry.lazy(".types")]] = UNSET
        covers: Optional[Annotated["Geometry", strawberry.lazy(".types")]] = UNSET
        crosses: Optional[Annotated["Geometry", strawberry.lazy(".types")]] = UNSET
        disjoint: Optional[Annotated["Geometry", strawberry.lazy(".types")]] = UNSET
        equals: Optional[Annotated["Geometry", strawberry.lazy(".types")]] = UNSET
        exacts: Optional[Annotated["Geometry", strawberry.lazy(".types")]] = UNSET
        intersects: Optional[Annotated["Geometry", strawberry.lazy(".types")]] = UNSET
        isempty: Optional[bool] = filter_field(description=f"Assignment test. {_SKIP_MSG}")
        isvalid: Optional[bool] = filter_field(description=f"Assignment test. {_SKIP_MSG}")
        overlaps: Optional[Annotated["Geometry", strawberry.lazy(".types")]] = UNSET
        touches: Optional[Annotated["Geometry", strawberry.lazy(".types")]] = UNSET
        within: Optional[Annotated["Geometry", strawberry.lazy(".types")]] = UNSET
        left: Optional[Annotated["Geometry", strawberry.lazy(".types")]] = UNSET
        right: Optional[Annotated["Geometry", strawberry.lazy(".types")]] = UNSET
        overlaps_left: Optional[Annotated["Geometry", strawberry.lazy(".types")]] = UNSET
        overlaps_right: Optional[Annotated["Geometry", strawberry.lazy(".types")]] = UNSET
        overlaps_above: Optional[Annotated["Geometry", strawberry.lazy(".types")]] = UNSET
        overlaps_below: Optional[Annotated["Geometry", strawberry.lazy(".types")]] = UNSET
        strictly_above: Optional[Annotated["Geometry", strawberry.lazy(".types")]] = UNSET
        strictly_below: Optional[Annotated["Geometry", strawberry.lazy(".types")]] = UNSET
