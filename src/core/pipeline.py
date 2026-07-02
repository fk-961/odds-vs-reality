from dataclasses import dataclass
from typing import Literal

from src.core.step import PipelineStep, StepExecutionResult

@dataclass
class Pipeline:
    name : str
    layer : str
    steps : list[PipelineStep]
    stop_on_fail : bool = True
    
@dataclass
class PipelineExecutionResult:
    name : str
    layer : str
    status : Literal["PASS", "WARNING", "FAIL"]
    warnings : int
    fails : int
    duration_seconds : float
    timestamp : str
    result : list[StepExecutionResult]