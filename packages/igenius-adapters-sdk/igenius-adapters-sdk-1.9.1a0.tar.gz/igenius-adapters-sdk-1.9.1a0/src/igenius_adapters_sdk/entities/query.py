from __future__ import annotations

import abc
from enum import Enum
from typing import Any, List, Optional, Tuple, Union

from pydantic import BaseModel, Field, root_validator

from igenius_adapters_sdk.entities import data, uri


class JoinType(str, Enum):
    INNER = "inner"
    LEFT_OUTER = "left-outer"
    RIGHT_OUTER = "right-outer"


class JoinPart(BaseModel):
    from_: From
    on: uri.AttributeUri


class Join(BaseModel):
    left: JoinPart
    right: JoinPart
    type: JoinType  # noqa: A003


From = Union[uri.CollectionUri, Join]
# see https://pydantic-docs.helpmanual.io/usage/postponed_annotations/#self-referencing-models
JoinPart.update_forward_refs()


class AliasableQuery(BaseModel):
    query: BaseQuery
    alias: str


With = List[AliasableQuery]
SqlTemplate = Tuple[str, Optional[List[Any]]]  # e.g. ("A = ? AND B = ?", [1,"test"])


class BaseQuery(BaseModel, abc.ABC):
    from_: From
    where: Optional[data.WhereExpression]
    order_by: Optional[List[data.OrderByAttribute]]
    limit: int = Field(None, ge=0)
    offset: int = Field(None, ge=0)
    with_: Optional[With] = None
    sql_template: Optional[SqlTemplate] = None


# see https://github.com/samuelcolvin/pydantic/issues/1298
AliasableQuery.update_forward_refs()


class SelectQuery(BaseQuery):
    attributes: List[Union[data.ProjectionAttribute, data.StaticValueAttribute]]
    distinct: bool = False


Aggregations = List[Union[data.CustomColumnAttribute, data.AggregationAttribute, data.StaticValueAttribute]]


class AggregationQuery(BaseQuery):
    aggregations: Aggregations


class GroupByQuery(BaseQuery):
    aggregations: Aggregations
    groups: List[data.BinningAttribute]
    bin_interpolation: Optional[bool] = None

    @root_validator
    def bin_interpolation_flag_validator(cls, values):
        flag = values.get("bin_interpolation")
        groups = values.get("groups")
        has_function_params = any([att.function_uri.function_params is not None for att in groups])
        if flag is None and has_function_params:
            values["bin_interpolation"] = True
        elif flag is True and not has_function_params:
            raise ValueError("bin_interpolation flag applys to binning attributes only")
        return values


Query = Union[GroupByQuery, AggregationQuery, SelectQuery]
