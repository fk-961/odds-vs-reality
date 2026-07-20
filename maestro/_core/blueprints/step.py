from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any
from uuid import UUID
from datetime import datetime

from ..runtime.context import (
    PipelineContext, ExecutionContext
)
from maestro.common.types import Status

class PipelineStep(ABC):
    name : str
    
    def success(
        self,
        output : dict[str, Any] | None = None
    ) -> StepResult:
        return StepResult(
            status = Status.PASS,
            step_results = output
        )
        
    def warning(
        self,
        msg : str,
        output : dict[str, Any] | None = None
    ) -> StepResult:
        return StepResult(
            status = Status.WARNING,
            step_results = output,
            message = msg,
        )
        
    def fail(
        self,
        msg : str,
        output : dict[str,Any] | None = None
    ) -> StepResult:
        return StepResult(
            status = Status.FAIL,
            step_results = output,
            message = msg,
        )
        
    
    @abstractmethod
    def run(
        self,
        ctx : PipelineContext,
        etx : ExecutionContext
    ) -> StepResult:
        pass
    
    
@dataclass
class StepResult:
    status : Status
    step_results : dict[str, Any] | None = None
    message : str | None = None
    error : str | None = None
    
@dataclass
class StepExecutionResult:
    run_id : UUID
    name : str
    timestamp : datetime
    duration_seconds : float
    status : Status
    step_results : dict[str, Any] | None = None
    message : str | None = None
    error : str | None = None