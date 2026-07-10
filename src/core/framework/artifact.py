"""
Instances of Artifact represent the combination of the necessary
steps required to create a specific table. It is defined by 3
stages: build, validate and persist each composed of steps.
"""
from dataclasses import dataclass
from uuid import UUID
from datetime import datetime

from src.core.framework.step import (
    PipelineStep, StepResult, StepExecutionResult
)
from src.core.framework.types import Status, Stage
from src.core.execution.context import PipelineContext
from src.core.execution.tracker import ExecutionTracker
from src.core.execution.execution import Execution

@dataclass
class Artifact:
    name : str
    builders : list[PipelineStep]
    validators : list[PipelineStep]
    persisters : list[PipelineStep]
    
    def get_builders(self) -> list[PipelineStep]:
        return self.builders
    
    def get_validators(self) -> list[PipelineStep]:
        return self.validators
    
    def get_persisters(self) -> list[PipelineStep]:
        return self.persisters
    

@dataclass
class ArtifactExecutionResult:
    run_id : UUID
    name : str
    timestamp : datetime
    duration_seconds : float
    
    
@dataclass
class ArtifactRunner:
    execution : Execution
    
    def run(
        self,
        artifact : Artifact,
        ctx : PipelineContext
    ) -> 
    
    def _run_stage(
        self,
        artifact : Artifact,
        stage : Stage,
        ctx : PipelineContext
    ) -> list[StepExecutionResult]:
        
        stage_logger = ctx.logger.child(
            artifact = artifact.name, stage = f"[{stage.value}]"
        )
        
        if stage == Stage.BUILD:
            steps = artifact.get_builders()
        elif stage == Stage.VALIDATE:
            steps = artifact.get_validators()
        elif stage == Stage.PERSIST:
            steps = artifact.get_persisters()
        
        stage_logger.info(
            "Scheduled build steps %s", len(steps)
        )
        
        stage_results = []
        for step in steps:
            stage_logger.info(
                "START step = %s", step.name
            )
            
            with ExecutionTracker() as tracker:
                try:
                    step_result = step.run(ctx)
                except Exception as e:
                    step_result = StepResult(
                        status = Status.FAIL,
                        message = "Unexpected Exception",
                        error = str(e)
                    )
            step_duration = tracker.duration
            
            stage_logger.log_status(
                step_result.status,
                "END step = %s status = %s duration = %s",
                step.name,
                step_result.status,
                step_duration
            )
                    
            stage_results.append(
                StepExecutionResult(
                    run_id = self.execution.run_id,
                    name = step.name,
                    timestamp = tracker.timestamp,
                    duration_seconds = step_duration,
                    status = step_result.status,
                    result = step_result.result,
                    message = step_result.message,
                    error = step_result.error
                )
            )
            
            if step_result.status == Status.FAIL and stage.abort_on_fail:
                stage_logger.error(
                    "ABORT [%s] reason step = %s failed, %s: %s",
                    stage.value,
                    step.name,
                    step_result.message,
                    step_result.error
                )
                
                return stage_results
            
        return stage_results
                    