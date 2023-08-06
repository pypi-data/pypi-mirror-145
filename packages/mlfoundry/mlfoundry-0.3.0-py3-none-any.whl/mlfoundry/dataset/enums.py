import enum
import typing

import pandas as pd
from pydantic import BaseModel, conlist

from mlfoundry.enums import FieldType


class DataSetType(enum.Enum):
    FEATURES = "features"
    ACTUALS = "actuals"
    PREDICTIONS = "predictions"
    SCHEMA = "schema"


class Schema(BaseModel):
    features: typing.Dict[str, FieldType]
    actuals: FieldType


class DataSet(BaseModel):
    features: pd.DataFrame
    actuals: typing.Optional[pd.Series] = None
    predictions: typing.Optional[pd.Series] = None

    dataset_schema: Schema

    class Config:
        arbitrary_types_allowed = True
