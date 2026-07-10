from dataclasses import dataclass
from uuid import UUID
from datetime import datetime

from src.core.framework.artifact import Artifact
from src.core.framework.types import Status

@dataclass
class Pipeline:
    name : str
    artifacts : list[Artifact]
    
@dataclass
class PipelineExecutionResult:
    run_id : UUID
    name : str
    timestamp : datetime
    duration_seconds : float
    status : Status
    warnings : int
    fails : int
    result : 