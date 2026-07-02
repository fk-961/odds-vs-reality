from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Literal, Any
from src.core.context import PipelineContext

class PipelineStep(ABC):
    name : str

    @abstractmethod
    def run(self, ctx : PipelineContext) -> StepResult:
        pass
    
@dataclass
class StepResult:
    status : Literal["PASS", "WARNING", "FAIL"]
    message : str | None = None
    error : str | None = None
    result : dict[str, Any] | None = None
    
@dataclass
class StepExecutionResult:
    name : str
    status : Literal["PASS", "WARNING", "FAIL"]
    duration_seconds : float
    timestamp : str
    message : str | None = None
    error : str | None = None
    result : dict[str, Any] | None = None