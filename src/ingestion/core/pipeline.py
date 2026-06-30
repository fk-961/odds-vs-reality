from dataclasses import dataclass

from src.ingestion.core.step import IngestionStep, StepExecutionResult

@dataclass
class IngestionPipeline:
    name : str
    steps : list[IngestionStep]
    
@dataclass
class IngestionExecutionResult:
    name : str
    status : str
    warnings : int
    fails : int
    duration_seconds : float
    timestamp : str
    result : list[StepExecutionResult]