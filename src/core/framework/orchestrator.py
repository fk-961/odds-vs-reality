from dataclasses import dataclass
from typing import Tuple
from uuid import UUID
from datetime import datetime

from src.core.framework.types import Status, get_overall_status
from src.core.execution.execution import Execution
from src.core.framework.pipeline import (
    Pipeline, PipelineExecutionResult, PipelineRunner
)
from src.core.execution.context import PipelineContext
from src.core.execution.tracker import ExecutionTracker

@dataclass
class Maestro:
    pipelines : list[Tuple[Pipeline, PipelineContext]]
    
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
    execution : Execution
    
    def execute(self, maestro : Maestro) -> MaestroExecutionResult:
        divider = "="*100
        maestro_logger = self.execution.logger.child(
            orchestrator = "maestro"
        )
        
        maestro_logger.info(
        """Starting execution
Pipelines Scheduled: %s
%s""",
            len(maestro.pipelines),
            divider
        )
        
        maestro_results = []
        
        with ExecutionTracker() as tracker:
            
            try:
                pipeline_runner = PipelineRunner(
                    self.execution
                )
                
                for pipeline, ctx in maestro.pipelines:
                    maestro_logger.info(
                        "Running [%s]\n%s",
                        pipeline.name,
                        divider
                    )
                    
                    pipeline_results = pipeline_runner.run(
                        pipeline, ctx
                    )
                    
                    maestro_results.append(pipeline_results)
                    
                    maestro_logger.log_status(
                        pipeline_results.status,
                        "[%s] execution finished status = %s duration = %s",
                        pipeline.name,
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
                    run_id = self.execution.get_run_id(),
                    status = status,
                    timestamp = tracker.timestamp,
                    duration_seconds = tracker.duration,
                    pipelines_scheduled = len(maestro.pipelines),
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
                    run_id = self.execution.get_run_id(),
                    status = Status.FAIL,
                    timestamp = tracker.timestamp,
                    duration_seconds = tracker.duration,
                    pipelines_scheduled = len(maestro.pipelines),
                    maestro_results = maestro_results
                )