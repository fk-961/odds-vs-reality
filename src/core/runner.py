from datetime import datetime
from time import perf_counter

from src.core.context import PipelineContext
from src.core.pipeline import Pipeline, PipelineExecutionResult
from src.core.step import StepResult, StepExecutionResult

class PipelineRunner:
    
    def run(
        self,
        pipeline : Pipeline,
        ctx : PipelineContext
    ) -> PipelineExecutionResult:
        
        ctx.logger.info(
            "[%s] START layer %s",
            pipeline.name, pipeline.layer
        )
        
        timestamp = datetime.now().isoformat()
        start = perf_counter()
        result = []
        status = "PASS"
        warnings = 0
        fails = 0
        
        for step in pipeline.steps:
            ctx.logger.info(
                "[%s] START step=%s",
                pipeline.layer, step.name
            )
            step_timestamp = datetime.now().isoformat()
            step_start = perf_counter()
            
            try:
                step_result = step.run(ctx)
            except Exception as e:
                ctx.logger.error(
                    "Unexpected exception in %s", step.name
                )
                step_result = StepResult(
                    status = "FAIL",
                    message = "Unexpected exception",
                    error = str(e)
                )
            
            step_duration = round(perf_counter() - step_start, 5)
            result.append(
                StepExecutionResult(
                    name = step.name,
                    status = step_result.status,
                    message = step_result.message,
                    error = step_result.error,
                    duration_seconds = step_duration,
                    timestamp = step_timestamp,
                    result = step_result.result
                )
            )
            
            if step_result.status == "FAIL":
                fails += 1
                
                if pipeline.stop_on_fail:
                    ctx.logger.error(
                        "ABORT [%s] because [%s] failed: reason %s",
                        pipeline.name,
                        step.name,
                        step_result.error
                    )
                    return PipelineExecutionResult(
                        name = pipeline.name,
                        layer= pipeline.layer,
                        status = "FAIL",
                        warnings = warnings,
                        fails = fails,
                        duration_seconds = round(perf_counter() - start, 5),
                        timestamp = timestamp,
                        result = result
                    )
                    
                status = "FAIL"
                
            if step_result.status == "WARNING" and status != "FAIL":
                warnings += 1
                status = "WARNING"

            ctx.logger.log_status(
                step_result.status,
                "[%s] END step=%s status %s duration %ss",
                pipeline.layer, step.name, step_result.status, step_duration
            )
                
            
        duration = round(perf_counter() - start, 5)
        
            
        ctx.logger.info("Pipeline finished: %s", pipeline.name)
        ctx.logger.log_status(
            status,
            "[%s] END pipeline status=%s duration=%.3fs warnings=%s fails=%s",
            pipeline.name,
            status,
            duration,
            warnings,
            fails
        )
        
        return PipelineExecutionResult(
            name = pipeline.name,
            layer = pipeline.layer,
            status = status,
            warnings = warnings,
            fails = fails,
            duration_seconds = duration,
            timestamp = timestamp,
            result = result
        )
            