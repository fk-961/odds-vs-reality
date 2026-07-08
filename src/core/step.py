from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Literal, Any

from src.core.status import Status
from src.core.pipeline import PipelineContext

@dataclass
class StepResult:
    status : Status
    error : str | None = None
    message : str | None = None
    result : dict[str, Any] | None = None

class PipelineStep(ABC):
    name : str
    
    @abstractmethod
    def run(self, ctx : PipelineContext) -> StepResult:
        pass
    
@dataclass
class StepExecutionResult:
    name : str
    status : Status
    timestamp : str
    duration_seconds : float
    error : str | None = None
    message : str | None = None
    result : dict[str, Any] | None = None