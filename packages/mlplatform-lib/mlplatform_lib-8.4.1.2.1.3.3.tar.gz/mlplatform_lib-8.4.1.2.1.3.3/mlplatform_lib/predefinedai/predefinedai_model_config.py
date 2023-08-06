from dataclasses import dataclass
from enum import Enum
import abc
from typing import List, Union


class PredefinedAIArgType(Enum):
    String = 'String'
    Integer = 'Integer'
    Float = 'Float'
    Categorical = 'Categorical'
    MultipleOf2 = 'MultipleOf2'


class PredefinedAIArg:
    @abc.abstractmethod
    def get_key(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_value(self):
        raise NotImplementedError


@dataclass
class PredefinedAIStringArg(PredefinedAIArg):
    key: str
    displayName: str
    description: str
    value: str

    def get_key(self):
        return self.key

    def get_value(self):
        return self.value


@dataclass
class PredefinedAIBoolArg(PredefinedAIArg):
    key: str
    displayName: str
    description: str
    value: bool

    def get_key(self):
        return self.key

    def get_value(self):
        return self.value


@dataclass
class PredefinedAIIntegerArg(PredefinedAIArg):
    key: str
    displayName: str
    description: str
    min: int
    max: int
    value: int
    unitStep: int
    type: PredefinedAIArgType = PredefinedAIArgType.Integer

    def get_key(self):
        return self.key

    def get_value(self):
        return self.value


@dataclass
class PredefinedAIFloatArg(PredefinedAIArg):
    key: str
    displayName: str
    description: str
    min: float
    max: float
    value: float
    unitStep: float
    type: PredefinedAIArgType = PredefinedAIArgType.Float

    def get_key(self):
        return self.key

    def get_value(self):
        return self.value


@dataclass
class PredefinedAIMultipleOf2Arg(PredefinedAIArg):
    key: str
    displayName: str
    description: str
    min: int
    max: int
    value: int
    unitStep: int
    type: PredefinedAIArgType = PredefinedAIArgType.MultipleOf2

    def get_key(self):
        return self.key

    def get_value(self):
        return self.value


@dataclass
class PredefinedAICategoricalValue:
    key: str
    displayName: str
    description: str


@dataclass
class PredefinedAICategoricalArg(PredefinedAIArg):
    key: str
    displayName: str
    description: str
    values: List[PredefinedAICategoricalValue]
    value: PredefinedAICategoricalValue
    type: PredefinedAIArgType = PredefinedAIArgType.Categorical

    def get_key(self):
        return self.key

    def get_value(self):
        return self.value.key


@dataclass
class HyperParameters:
    algorithmHyperParameters: List[
        Union[PredefinedAIBoolArg, PredefinedAIIntegerArg, PredefinedAIFloatArg, PredefinedAIMultipleOf2Arg, PredefinedAICategoricalArg]]
    modelHyperParameters: List[
        Union[PredefinedAIBoolArg, PredefinedAIIntegerArg, PredefinedAIFloatArg, PredefinedAIMultipleOf2Arg, PredefinedAICategoricalArg]]
    samplingHyperParameters: List[
        Union[PredefinedAIBoolArg, PredefinedAIIntegerArg, PredefinedAIFloatArg, PredefinedAIMultipleOf2Arg, PredefinedAICategoricalArg]]
    metricHyperParameters: List[
        Union[PredefinedAIBoolArg, PredefinedAIIntegerArg, PredefinedAIFloatArg, PredefinedAIMultipleOf2Arg, PredefinedAICategoricalArg]]

    def __post_init__(self):
        self.hyperparameter_dict = {}
        for hp_group in self.__annotations__.keys():
            for hp in self.__getattribute__(hp_group):
                self.hyperparameter_dict[hp.get_key()] = hp.get_value()


@dataclass
class Config:
    args: List[
        Union[
            PredefinedAIStringArg, PredefinedAIBoolArg, PredefinedAIIntegerArg, PredefinedAIFloatArg, PredefinedAIMultipleOf2Arg, PredefinedAICategoricalArg]]


@dataclass
class PredefinedAIModelConfig:
    key: str
    displayName: str
    description: str
    hyperParameters: HyperParameters
    train: Config
    retrain: Config
    inference: Config
    serving: Config

    def _get_hyperparameters_dict(self) -> dict:
        return self.hyperParameters.__getattribute__('hyperparameter_dict')

    def _get_args_dict(self, stage) -> dict:
        args_dict = {}
        args = self.__getattribute__(stage).__getattribute__('args')
        for arg in args:
            args_dict[arg.get_key()] = arg.get_value()
        return args_dict

