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
        
        etx.cascade_logger(
            etx.logger.child(
                artifact = artifact.name
            )
        )
        
        etx.logger.info("START Artifact lifecycle")
        
        artifact_results = []
        
        with ExecutionTracker() as tracker:
            
            try:
                
                stages = artifact.get_stages()
                for stage in stages:
                    etx.logger.info("Staging [%s] steps", stage.value)

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
                            "ABORT [%s] %s: %s",
                            stage.value,
                            stage_results.message,
                            stage_results.error
                        )
                        
                        for remaining in stages[stages.index(stage)+1:]:
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
                    artifact_results = artifact_results
                )
            
            except Exception as e:
                message = "Unexpected Exception"
                error = f"{type(e).__name__}: {e}"
                etx.logger.error(
                    "ABORT %s, %s: %s",
                    artifact.name,
                    message,
                    error
                )
                
                return ArtifactExecutionResult(
                    run_id = etx.get_run_id(),
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
        ctx : PipelineContext,
        etx : ExecutionContext
    ) -> StageExecutionResult:
        
        etx.cascade_logger(
            etx.logger.child(
                stage = f"{stage.value}"
            )
        )
        
        steps = {
            Stage.BUILD: artifact.get_builders(),
            Stage.VALIDATE: artifact.get_validators(),
            Stage.PERSIST: artifact.get_persisters(),
        }[stage]
            
        etx.logger.info(
            "Scheduled steps %s", len(steps)
        )
        
        stage_results = []
        steps_attempted = 0
        warnings = 0
        
        with ExecutionTracker() as stage_tracker:
            
            try:
                for step in steps:
                    etx.logger.info(
                        "START step = %s", step.name
                    )
                    
                    with ExecutionTracker() as step_tracker:
                        try:
                            step_result = step.run(ctx, etx)
                        except Exception as e:
                            step_result = StepResult(
                                status = Status.FAIL,
                                message = "Unexpected Exception",
                                error = f"{type(e).__name__}: {e}"
                            )
                    steps_attempted += 1
                    
                    stage_results.append(StepExecutionResult(
                        run_id = etx.get_run_id(),
                        name = step.name,
                        timestamp = step_tracker.timestamp,
                        duration_seconds = step_tracker.duration,
                        status = step_result.status,
                        step_results = step_result.step_results,
                        message = step_result.message,
                        error = step_result.error
                    ))
                            
                    if step_result.status == Status.FAIL and stage.abort_on_fail:
                        etx.logger.error(
                            "ABORT %s reason step = %s failed, %s: %s",
                            stage.value,
                            step.name,
                            step_result.message,
                            step_result.error
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
                            message = step_result.message,
                            error = step_result.error
                        )
                    
                    else:
                        if step_result.status == Status.WARNING:
                            warnings += 1
                        etx.logger.log_status(
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
            
            except Exception as e:
                message = "Unexpected Exception"
                error = f"{type(e).__name__}: {e}"
                etx.logger.error(
                    "ABORT [%s] %s: %s",
                    stage.value,
                    message,
                    error
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
                    message = message,
                    error = error
                )
                    