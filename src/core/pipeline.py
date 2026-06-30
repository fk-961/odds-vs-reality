from dataclasses import dataclass

from src.core.step import PipelineStep, StepExecutionResult

@dataclass
class Pipeline:
    name : str
    layer : str
    steps : list[PipelineStep]
    
@dataclass
class PipelineExecutionResult:
    name : str
    layer : str
    status : str
    warnings : int
    fails : int
    duration_seconds : float
    timestamp : str
    result : list[StepExecutionResult]