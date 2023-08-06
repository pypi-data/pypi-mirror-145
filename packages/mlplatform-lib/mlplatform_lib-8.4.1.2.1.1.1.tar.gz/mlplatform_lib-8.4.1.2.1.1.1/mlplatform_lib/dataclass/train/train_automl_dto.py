from dataclasses import dataclass


@dataclass
class TrainAutomlDto:
    id: int
    experiment_id: int
    workflow: Dict[str, str]
    experiment_type: str
    is_active_learning: bool
    active_learning_row: str
    
    
