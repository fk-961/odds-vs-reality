from dataclasses import dataclass
from typing import Tuple
from uuid import UUID
from datetime import datetime

from src.core.framework.types import Status, get_overall_status
from src.core.framework.pipeline import (
    Pipeline, PipelineExecutionResult, PipelineRunner
)
from src.core.execution.context import PipelineContext
from src.core.execution.tracker import ExecutionTracker

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
    maestro_results: list[PipelineExecutionResult] | None = None
    message : str | None = None
    error : str | None = None
    
    
@dataclass
class MaestroRunner:
    
    def execute(
        self,
        maestro : Maestro,
        etx : ExecutionTracker
    ) -> MaestroExecutionResult:
        divider = "="*100
        maestro_logger = etx.logger.child(
            orchestrator = "maestro"
        )
        
        maestro_logger.info(
        """Starting execution
Pipelines Scheduled: %s
%s""",
            len(maestro.jobs),
            divider
        )
        
        maestro_results = []
        
        with ExecutionTracker() as tracker:
            
            try:
                pipeline_runner = PipelineRunner()
                
                for job in maestro.jobs:
                    maestro_logger.info(
                        "Running [%s]\n%s",
                        job.pipeline.name,
                        divider
                    )
                    
                    pipeline_results = pipeline_runner.run(
                        job.pipeline, job.context, etx
                    )
                    
                    maestro_results.append(pipeline_results)
                    
                    maestro_logger.log_status(
                        pipeline_results.status,
                        "[%s] execution finished status = %s duration = %s",
                        job.pipeline.name,
                        pipeline_results.status.value,
                        pipeline_results.duration_seconds
                    )
                    
                status = get_overall_status(maestro_results)
                
                maestro_logger.log_status(
                    status,
                    "\n%s\nExecution Summary: status = %s duration = %s",
                    divider,
                    status.value,
                    tracker.duration
                )
            
                return MaestroExecutionResult(
                    run_id = etx.get_run_id(),
                    status = status,
                    timestamp = tracker.timestamp,
                    duration_seconds = tracker.duration,
                    pipelines_scheduled = len(maestro.jobs),
                    maestro_results = maestro_results
                )
                
            except Exception as e:
                message = "Unexpected Exception"
                error = str(e)
                
                maestro_logger.error(
                    "ABORT Execution, %s: %s",
                    message,
                    error
                )
                
                return MaestroExecutionResult(
                    run_id = etx.get_run_id(),
                    status = Status.FAIL,
                    timestamp = tracker.timestamp,
                    duration_seconds = tracker.duration,
                    pipelines_scheduled = len(maestro.jobs),
                    maestro_results = maestro_results,
                    message = message,
                    error = error
                )