from maestro._core.blueprints.artifact import (
    Artifact, ArtifactExecutionResult, StageExecutionResult
)
from maestro._core.blueprints.step import (
    StepResult, StepExecutionResult
)
from maestro._core.runtime.context import (
    PipelineContext, ExecutionContext
)
from maestro.common.types import (
    Status, Stage, get_overall_status
)
from ..tracker import ExecutionTracker

class ArtifactRunner:
    
    def run(
        self,
        artifact : Artifact,
        ctx : PipelineContext,
        etx : ExecutionContext
    ) -> ArtifactExecutionResult:
        
        with ExecutionTracker() as tracker:
            try:
                artifact_results = self._run(
                    artifact, ctx, etx
                )
            except Exception as e:
                message = "Unhandled framework exception"
                error = f"{type(e).__name__}: {e}"
                
                etx.logger.error(
                    "ABORT %s lifecycle: %s: %s",
                    artifact.name,
                    message,
                    error
                )
                
                artifact_results = ArtifactExecutionResult(
                    run_id = etx.get_run_id(),
                    name = artifact.name,
                    timestamp = tracker.timestamp,
                    duration_seconds = tracker.duration,
                    status = Status.FAIL,
                    message = message,
                    error = error
                )
                
            return artifact_results
                
    
    def _run(
        self,
        artifact : Artifact,
        ctx : PipelineContext,
        etx : ExecutionContext
    ) -> ArtifactExecutionResult:
        
        etx.cascade_logger(
            etx.logger.child(
                artifact = artifact.name,
                stage = None
            )
        )
        
        etx.logger.info("START Artifact lifecycle")
        
        artifact_results = []
        
        with ExecutionTracker() as tracker:
            
            stages = artifact.get_stages()
            for stage in stages:
                etx.logger.info("STAGING [%s] steps", stage.value)
                
                stage_results = self._run_stage(
                    artifact, stage, ctx, etx
                )
                
                artifact_results.append(stage_results)
                
                etx.logger.log_status(
                    stage_results.status,
                    "END [%s] stage status = %s duration = %s",
                    stage.value,
                    stage_results.status.value,
                    stage_results.duration_seconds
                )
                
                if stage_results.status == Status.FAIL:
                    etx.logger.error(
                        "ABORT Artifact %s lifecycle reason: [%s] failed",
                        artifact.name,
                        stage.value
                    )
                    
                    for remaining in stages[stages.index(stage) + 1:]:
                        etx.logger.info(
                            "Skipping [%s]",
                            remaining.value
                        )
                        
                        artifact_results.append(
                            StageExecutionResult(
                                run_id=etx.get_run_id(),
                                stage=remaining,
                                artifact_name=artifact.name,
                                scheduled_steps=0,
                                timestamp=tracker.timestamp,
                                duration_seconds=0,
                                status=Status.SKIPPED,
                                steps_attempted=0,
                                steps_warnings_count=0,
                                message="Skipped",
                                error=f"Previous stage [{stage.value}] failed"
                            )
                        )
                        
                    break
                    
            overall_status = get_overall_status(
                artifact_results
            )
                    
            return ArtifactExecutionResult(
                run_id = etx.get_run_id(),
                name = artifact.name,
                timestamp = tracker.timestamp,
                duration_seconds = tracker.duration,
                status = overall_status,
                artifact_results = artifact_results,
            )
        
                
    
    def _run_stage(
        self,
        artifact : Artifact,
        stage : Stage,
        ctx : PipelineContext,
        etx : ExecutionContext
    ) -> StageExecutionResult:
        
        stage_logger = etx.logger.child(
            stage = f"{stage.value}"
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
            
            for step in steps:
                stage_logger.info(
                    "START step = %s", step.name
                )
                
                with ExecutionTracker() as step_tracker:
                    
                    try:
                        step_results = step.run(ctx, etx)
                        
                    except Exception as e:
                        error = f"{type(e).__name__}: {e}"
                        message = "Unhandled Exception"
                        stage_logger.error(
                            "step = %s FAILED: %s: %s",
                            step.name,
                            message,
                            error
                        )
                        step_results = StepResult(
                            status = Status.FAIL,
                            message = message,
                            error = error
                        )
                    
                    steps_attempted += 1
                    stage_results.append(StepExecutionResult(
                        run_id = etx.get_run_id(),
                        name = step.name,
                        timestamp = step_tracker.timestamp,
                        duration_seconds = step_tracker.duration,
                        status = step_results.status,
                        step_results = step_results.step_results,
                        message = step_results.message,
                        error = step_results.error
                    ))
        
                            
                    if step_results.status == Status.FAIL and stage.abort_on_fail:
                        stage_logger.error(
                            "ABORT %s reason step = %s failed",
                            stage.value,
                            step.name,
                        )
                        
                        return StageExecutionResult(
                            run_id = etx.get_run_id(),
                            stage = stage,
                            artifact_name = artifact.name,
                            scheduled_steps = len(steps),
                            timestamp = stage_tracker.timestamp,
                            duration_seconds = stage_tracker.duration,
                            status = Status.FAIL,
                            steps_attempted = steps_attempted,
                            steps_warnings_count = warnings,
                            stage_results = stage_results,
                            message = step_results.message,
                            error = step_results.error
                        )
                    
                    else:
                        if step_results.status == Status.WARNING:
                            warnings += 1
                        stage_logger.log_status(
                            step_results.status,
                            "END step = %s status = %s duration = %s",
                            step.name,
                            step_results.status.value,
                            step_tracker.duration
                        )
                        
            
            overall_status = get_overall_status(
                stage_results
            )
                    
            return StageExecutionResult(
                run_id = etx.get_run_id(),
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
            