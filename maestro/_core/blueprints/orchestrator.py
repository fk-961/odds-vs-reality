from dataclasses import dataclass
from typing import Tuple
from uuid import UUID
from datetime import datetime

from maestro.common.types import Status
from .pipeline import (
    Pipeline, PipelineExecutionResult
)
from ..runtime.context import PipelineContext

@dataclass
class PipelineExecution:
    pipeline : Pipeline
    context : PipelineContext
    
@dataclass
class Maestro:
    jobs : list[PipelineExecution]
    
@dataclass
class MaestroExecutionResult:
    run_id : UUID
    status : Status
    timestamp : datetime
    duration_seconds : float
    pipelines_scheduled : int
    artifacts_count : int
    artifacts_passed : int
    artifacts_skipped : int
    artifacts_failed : int
    maestro_results: list[PipelineExecutionResult] | None = None
    message : str | None = None
    error : str | None = None
