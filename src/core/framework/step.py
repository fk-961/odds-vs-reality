from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any
from uuid import UUID
from datetime import datetime

from src.core.execution.context import PipelineContext
from src.core.framework.types import Status

class PipelineStep(ABC):
    name : str
    
    @abstractmethod
    def run(self, ctx : PipelineContext) -> StepResult:
        pass
    
    
@dataclass
class StepResult:
    status : Status
    result : dict[str, Any] | None = None
    message : str | None = None
    error : str | None = None
    
@dataclass
class StepExecutionResult:
    run_id : UUID
    name : str
    timestamp : datetime
    duration_seconds : float
    status : Status
    result : dict[str, Any] | None = None
    message : str | None = None
    error : str | None = None