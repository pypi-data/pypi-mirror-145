from dataclasses import dataclass, field


@dataclass
class ExperimentDataObjectInfo:
    key: str
    doId: int = None
    doName: str = None
