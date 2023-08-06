from dataclasses import dataclass, field


@dataclass
class ExperimentDataObjectInfo:
    key: str
    doId: int = field(default=None)
    doName: str = field(default=None)
