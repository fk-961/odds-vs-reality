"""
Instances of Artifact represent the combination of the necessary
steps required to create a specific table. It is defined by 3
stages: build, validate and persist each composed of steps.
"""
from dataclasses import dataclass, field
from uuid import UUID
from datetime import datetime

from src.core.framework.step import (
    PipelineStep, StepResult, StepExecutionResult
)
from src.core.framework.types import (
    Status, Stage, get_overall_status
)
from src.core.execution.context import PipelineContext
from src.core.execution.tracker import ExecutionTracker
from src.core.execution.execution import Execution
from src.core.execution.logger import PipelineLogger

@dataclass
class Artifact:
    name : str
    builders : list[PipelineStep]
    validators : list[PipelineStep]
    persisters : list[PipelineStep]
    stages : list[Stage] = field(
        default_factory = lambda: [
            Stage.BUILD, Stage.VALIDATE, Stage.PERSIST
        ],
        init = False
    )
    
    def get_builders(self) -> list[PipelineStep]:
        return self.builders
    
    def get_validators(self) -> list[PipelineStep]:
        return self.validators
    
    def get_persisters(self) -> list[PipelineStep]:
        return self.persisters
    
    def get_stages(self) -> list[Stage]:
        return self.stages
    

@dataclass
class StageExecutionResult:
    run_id : UUID
    stage : Stage
    artifact_name : str
    scheduled_steps : int
    timestamp : datetime
    duration_seconds : float
    status : Status
    steps_attempted : int
    steps_warnings_count : int
    stage_results : list[StepExecutionResult] | None = None
    message : str | None = None
    error : str | None = None
    
@dataclass
class ArtifactExecutionResult:
    run_id : UUID
    name : str
    timestamp : datetime
    duration_seconds : float
    status : Status
    artifact_results : list[StageExecutionResult] | None = None
    message : str | None = None
    error : str | None = None
    
    
@dataclass
class ArtifactRunner:
    execution : Execution
    
    def run(
        self,
        artifact : Artifact,
        ctx : PipelineContext
    ) -> ArtifactExecutionResult:
        
        artifact_logger = self.execution.logger.child(
            artifact = artifact.name
        )
        
        artifact_logger.info("START Artifact lifecycle")
        
        artifact_results = []
        
        with ExecutionTracker() as tracker:
            
            try:
                
                stages = artifact.get_stages()
                for stage in stages:
                    artifact_logger.info("START [%s] stage", stage.value)

                    stage_results = self._run_stage(
                        artifact, stage, artifact_logger, ctx
                    )
                        
                    artifact_results.append(stage_results)
                    
                    artifact_logger.log_status(
                        stage_results.status,
                        "END [%s] stage status = %s duration = %s",
                        stage.value,
                        stage_results.status.value,
                        stage_results.duration_seconds
                    )
                    
                    if stage_results.status == Status.FAIL:
                        artifact_logger.error(
                            "ABORT [%s] %s: %s",
                            stage.value,
                            stage_results.message,
                            stage_results.error
                        )
                        
                        for remaining in stages[stages.index(stage)+1:]:
                            artifact_logger.info(
                                "Skipping [%s]",
                                remaining.value
                            )
                        
                        break
                    
                overall_status = get_overall_status(
                    artifact_results
                )
                
                return ArtifactExecutionResult(
                    run_id = self.execution.get_run_id(),
                    name = artifact.name,
                    timestamp = tracker.timestamp,
                    duration_seconds = tracker.duration,
                    status = overall_status,
                    artifact_results = artifact_results
                )
            
            except Exception as e:
                message = "Unexpected Exception"
                error = str(e)
                artifact_logger.error(
                    "ABORT %s, %s: %s",
                    artifact.name,
                    message,
                    error
                )
                
                return ArtifactExecutionResult(
                    run_id = self.execution.get_run_id(),
                    name = artifact.name,
                    timestamp = tracker.timestamp,
                    duration_seconds = tracker.duration,
                    status = Status.FAIL,
                    artifact_results = artifact_results,
                    message = message,
                    error = error
                )
                
    
    def _run_stage(
        self,
        artifact : Artifact,
        stage : Stage,
        logger : PipelineLogger,
        ctx : PipelineContext
    ) -> StageExecutionResult:
        
        stage_logger = logger.child(
            stage = f"[{stage.value}]"
        )
        
        steps = {
            Stage.BUILD: artifact.get_builders(),
            Stage.VALIDATE: artifact.get_validators(),
            Stage.PERSIST: artifact.get_persisters(),
        }[stage]
            
        stage_logger.info(
            "Scheduled steps %s", len(steps)
        )
        
        stage_results = []
        steps_attempted = 0
        warnings = 0
        
        with ExecutionTracker() as stage_tracker:
            
            try:
                for step in steps:
                    stage_logger.info(
                        "START step = %s", step.name
                    )
                    
                    with ExecutionTracker() as step_tracker:
                        try:
                            step_result = step.run(ctx)
                        except Exception as e:
                            step_result = StepResult(
                                status = Status.FAIL,
                                message = "Unexpected Exception",
                                error = str(e)
                            )
                    steps_attempted += 1
                    
                    stage_results.append(StepExecutionResult(
                        run_id = self.execution.get_run_id(),
                        name = step.name,
                        timestamp = step_tracker.timestamp,
                        duration_seconds = step_tracker.duration,
                        status = step_result.status,
                        step_results = step_result.step_results,
                        message = step_result.message,
                        error = step_result.error
                    ))
                            
                    if step_result.status == Status.FAIL and stage.abort_on_fail:
                        stage_logger.error(
                            "ABORT reason step = %s failed, %s: %s",
                            step.name,
                            step_result.message,
                            step_result.error
                        )
                        
                        return StageExecutionResult(
                            run_id = self.execution.get_run_id(),
                            stage = stage,
                            artifact_name = artifact.name,
                            scheduled_steps = len(steps),
                            timestamp = stage_tracker.timestamp,
                            duration_seconds = stage_tracker.duration,
                            status = Status.FAIL,
                            steps_attempted = steps_attempted,
                            steps_warnings_count = warnings,
                            stage_results = stage_results,
                            message = step_result.message,
                            error = step_result.error
                        )
                    
                    else:
                        if step_result.status == Status.WARNING:
                            warnings += 1
                        stage_logger.log_status(
                            step_result.status,
                            "END step = %s status = %s duration = %s",
                            step.name,
                            step_result.status.value,
                            step_tracker.duration
                        )
                        
            
                overall_status = get_overall_status(
                    stage_results
                )
                
                return StageExecutionResult(
                    run_id = self.execution.get_run_id(),
                    stage = stage,
                    artifact_name = artifact.name,
                    scheduled_steps = len(steps),
                    timestamp = stage_tracker.timestamp,
                    duration_seconds = stage_tracker.duration,
                    status = overall_status,
                    steps_attempted = steps_attempted,
                    steps_warnings_count = warnings,
                    stage_results = stage_results
                )
            
            except Exception as e:
                message = "Unexpected Exception"
                error = str(e)
                stage_logger.error(
                    "ABORT [%s] %s: %s",
                    stage.value,
                    message,
                    error
                )
                
                return StageExecutionResult(
                    run_id = self.execution.get_run_id(),
                    stage = stage,
                    artifact_name = artifact.name,
                    scheduled_steps = len(steps),
                    timestamp = stage_tracker.timestamp,
                    duration_seconds = stage_tracker.duration,
                    status = Status.FAIL,
                    steps_attempted = steps_attempted,
                    steps_warnings_count = warnings,
                    stage_results = stage_results,
                    message = message,
                    error = error
                )
                    