from dataclasses import dataclass
from uuid import UUID
from datetime import datetime

from .artifact import (
    Artifact, ArtifactExecutionResult
)
from maestro.common.types import Status

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
    artifacts_scheduled : int
    artifacts_passed : int
    artifacts_failed : int
    artifacts_skipped : int
    pipeline_results : list[ArtifactExecutionResult] | None = None
    message : str | None = None
    error : str | None = None