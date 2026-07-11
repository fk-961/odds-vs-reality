from dataclasses import dataclass
from uuid import UUID
from datetime import datetime

from src.core.framework.artifact import (
    Artifact, ArtifactExecutionResult, ArtifactRunner
)
from src.core.framework.types import Status, get_overall_status
from src.core.execution.execution import Execution
from src.core.execution.tracker import ExecutionTracker
from src.core.execution.context import PipelineContext


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
    artifacts_failed : int
    pipeline_results : list[ArtifactExecutionResult] | None = None
    message : str | None = None
    error : str | None = None
    
@dataclass
class PipelineRunner:
    execution : Execution
    
    def run(
        self,
        pipeline : Pipeline,
        ctx : PipelineContext
    ) -> PipelineExecutionResult:
        
        pipeline_logger = self.execution.logger.child(
            pipeline = pipeline.name
        )
        pipeline_logger.info(
            "START pipeline execution, artifacts scheduled: %s",
            len(pipeline.artifacts)
        )
        
        pipeline_results = []
        fails = 0
        
        with ExecutionTracker() as tracker:
            
            try:
                artifact_runner = ArtifactRunner(
                    execution = self.execution
                )
                
                for artifact in pipeline.artifacts:
                        pipeline_logger.info(
                            "Staging artifact [%s]",
                            artifact.name
                        )
                        
                        artifact_results = artifact_runner.run(
                            artifact, ctx
                        )
                        
                        pipeline_results.append(artifact_results)
                        
                        pipeline_logger.log_status(
                            artifact_results.status,
                            "Executed [%s] lifecycle status = %s duration = %s",
                            artifact.name,
                            artifact_results.status.value,
                            artifact_results.duration_seconds
                        )
                        
                        if artifact_results.status == Status.FAIL:
                            fails += 1
                            
                status = get_overall_status(pipeline_results)
                            
                return PipelineExecutionResult(
                    run_id = self.execution.get_run_id(),
                    name = pipeline.name,
                    timestamp = tracker.timestamp,
                    duration_seconds = tracker.duration,
                    status = status,
                    artifacts_scheduled = len(pipeline.artifacts),
                    artifacts_failed = fails,
                    pipeline_results = pipeline_results,
                )
                        
            except Exception as e:
                message = "Unexpected Exception"
                error = str(e)
                
                pipeline_logger.error(
                    "ABORT pipeline, %s: %s",
                    message,
                    error
                )
                
                return PipelineExecutionResult(
                    run_id = self.execution.get_run_id(),
                    name = pipeline.name,
                    timestamp = tracker.timestamp,
                    duration_seconds = tracker.duration,
                    status = Status.FAIL,
                    artifacts_scheduled = len(pipeline.artifacts),
                    artifacts_failed = fails,
                    message = message,
                    error = error
                )