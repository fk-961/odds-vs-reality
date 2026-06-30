from abc import ABC, abstractmethod
from dataclasses import dataclass
from src.core.context import PipelineContext

class PipelineStep(ABC):
    name : str

    @abstractmethod
    def run(self, ctx : PipelineContext) -> StepResult:
        pass
    
@dataclass
class StepResult:
    status : str
    result : dict[str, any]
    
@dataclass
class StepExecutionResult:
    name : str
    status : str
    duration_seconds : float
    timestamp : str
    result : dict[str, any]