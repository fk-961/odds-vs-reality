from maestro._core.blueprints.pipeline import (
    Pipeline, PipelineExecutionResult
)
from maestro._core.blueprints.artifact import (
    ArtifactExecutionResult
)
from maestro._core.runtime.context import (
    PipelineContext, ExecutionContext
)
from ..tracker import ExecutionTracker
from ..runners.artifact import ArtifactRunner
from maestro.common.types import (
    Status, get_overall_status
)

class PipelineRunner:
    
    def run(
        self,
        pipeline : Pipeline,
        ctx : PipelineContext,
        etx : ExecutionContext
    ) -> PipelineExecutionResult:
        
        etx.cascade_logger(
            etx.logger.child(
                pipeline = pipeline.name
            )
        )
                            
        etx.logger.info(
            "START pipeline execution, artifacts scheduled: %s",
            len(pipeline.artifacts)
        )
        
        pipeline_results = []
        passed = 0
        fails = 0
        skipped = 0
        
        with ExecutionTracker() as tracker:
            
            try:
                artifact_runner = ArtifactRunner()
                
                for artifact in pipeline.artifacts:
                        etx.logger.info(
                            "Staging artifact [%s]",
                            artifact.name
                        )
                        
                        persisted_artifacts = set(etx.get_persisted_artifacts())
                        if all(dep in persisted_artifacts for dep in artifact.get_dependencies()):
                            etx.logger.info(
                                "All dependencies found, starting execution"
                            )
                        
                            artifact_results = artifact_runner.run(
                                artifact, ctx, etx
                            )
                            
                            if artifact_results.status == Status.FAIL:
                                fails += 1
                            if artifact_results.status == Status.PASS:
                                passed += 1
                                etx.add_successful_artifact(artifact.name)
                            
                            pipeline_results.append(artifact_results)
                            
                            etx.logger.log_status(
                                artifact_results.status,
                                "Executed [%s] lifecycle status = %s duration = %s",
                                artifact.name,
                                artifact_results.status.value,
                                artifact_results.duration_seconds
                            )
                            
                        else:
                            skipped += 1
                            
                            etx.logger.warning(
                                "SKIPPING %s execution: missing dependencies",
                                artifact.name
                            )
                            
                            pipeline_results.append(
                                ArtifactExecutionResult(
                                    run_id = etx.get_run_id(),
                                    name = artifact.name,
                                    timestamp = tracker.timestamp,
                                    duration_seconds = tracker.duration,
                                    status = Status.SKIPPED,
                                    message = "Skipping execution",
                                    error = "Missing dependencies"
                                )
                            )
                            
                status = get_overall_status(pipeline_results)
                            
                return PipelineExecutionResult(
                    run_id = etx.get_run_id(),
                    name = pipeline.name,
                    timestamp = tracker.timestamp,
                    duration_seconds = tracker.duration,
                    status = status,
                    artifacts_scheduled = len(pipeline.artifacts),
                    artifacts_passed = passed,
                    artifacts_failed = fails,
                    artifacts_skipped = skipped,
                    pipeline_results = pipeline_results,
                )
                        
            except Exception as e:
                message = "Unexpected Exception"
                error = f"{type(e).__name__}: {e}"
                
                etx.logger.error(
                    "ABORT pipeline, %s: %s",
                    message,
                    error
                )
                
                return PipelineExecutionResult(
                    run_id = etx.get_run_id(),
                    name = pipeline.name,
                    timestamp = tracker.timestamp,
                    duration_seconds = tracker.duration,
                    status = Status.FAIL,
                    artifacts_scheduled = len(pipeline.artifacts),
                    artifacts_passed = passed,
                    artifacts_failed = fails,
                    artifacts_skipped = skipped,
                    message = message,
                    error = error
                )