from dataclasses import dataclass
from typing import Tuple
from uuid import UUID
from datetime import datetime

from src.core.framework.types import Status, get_overall_status
from src.core.framework.pipeline import (
    Pipeline, PipelineExecutionResult, PipelineRunner
)
from src.core.execution.context import (
    PipelineContext, ExecutionContext
)
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
    artifacts_count : int
    artifacts_passed : int
    artifacts_skipped : int
    artifacts_failed : int
    maestro_results: list[PipelineExecutionResult] | None = None
    message : str | None = None
    error : str | None = None
    
    
@dataclass
class MaestroRunner:
    
    def run(
        self,
        maestro : Maestro,
        etx : ExecutionContext
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
        artifacts_count = 0
        artifacts_passed = 0
        artifacts_skipped = 0
        artifacts_failed = 0
        
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
                    artifacts_count += pipeline_results.artifacts_scheduled
                    artifacts_passed += pipeline_results.artifacts_passed
                    artifacts_skipped += pipeline_results.artifacts_skipped
                    artifacts_failed += pipeline_results.artifacts_failed
                    
                    maestro_results.append(pipeline_results)
                    
                    maestro_logger.log_status(
                        pipeline_results.status,
                        "[%s] execution finished status = %s duration = %s",
                        job.pipeline.name,
                        pipeline_results.status.value,
                        pipeline_results.duration_seconds
                    )
                    
                status = get_overall_status(maestro_results)
                
                maestro_logger.info(
                    "\n%s\nMaestro execution done for scheduled pipelines",
                    divider
                )
                maestro_logger.log_status(
                    status,
                    """\n%s
Execution summary\n
Pipelines : %s
Artifacts : %s
Passed : %s
Skipped : %s
Failed : %s

Duration : %s s
%s""",
                    divider,
                    len(maestro.jobs),
                    artifacts_count,
                    artifacts_passed,
                    artifacts_skipped,
                    artifacts_failed,
                    tracker.duration,
                    divider
                )
            
                return MaestroExecutionResult(
                    run_id = etx.get_run_id(),
                    status = status,
                    timestamp = tracker.timestamp,
                    duration_seconds = tracker.duration,
                    pipelines_scheduled = len(maestro.jobs),
                    artifacts_count = artifacts_count,
                    artifacts_passed = artifacts_passed,
                    artifacts_skipped = artifacts_skipped,
                    artifacts_failed = artifacts_failed,
                    maestro_results = maestro_results
                )
                
            except Exception as e:
                message = "Unexpected Exception"
                error = f"{type(e).__name__}: {e}"
                
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