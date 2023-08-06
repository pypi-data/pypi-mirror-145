from dataclasses import dataclass
from enum import Enum
from typing import List, Union
from typing_extensions import TypedDict


class StrEnum(str, Enum):
    def __repr__(self):
        return str(self.name)

    def __str__(self):
        return str(self.name)


class ColumnType(StrEnum):
    Numerical = 'Numerical'
    Categorical = 'Categorical'
    Textual = 'Textual'
    TimeStamp = 'TimeStamp'
    Auto = 'Auto'


@dataclass
class Column:
    name: str = ''
    type: ColumnType = ColumnType.Auto


class ColumnDict(TypedDict):
    name: str
    type: ColumnType


class DataConfigurationType(StrEnum):
    Data = 'Data'
    Column = 'Column'
    Columns = 'Columns'


class DefinedConstraint(StrEnum):
    ColumnNumberConstraint = 'ColumnNumberConstraint'
    ColumnRequiredConstraint = 'ColumnRequiredConstraint'
    RecordNumberConstraint = 'RecordNumberConstraint'


@dataclass
class Constraint:
    dataKey: str
    key: str
    type: DataConfigurationType
    constraint: DefinedConstraint
    value: int


@dataclass
class DataConfiguration:
    displayName: str
    key: str
    type: DataConfigurationType
    value: Union[Column, List[Column]]
    required: bool
    constraints: List[Constraint]
    description: str


@dataclass
class PredefinedAIDataConfig:
    displayName: str
    key: str
    configurations: List[DataConfiguration]
    description: str
    constraints: List[Constraint]

