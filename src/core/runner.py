from datetime import datetime
from time import perf_counter

from src.core.context import PipelineContext
from src.core.pipeline import Pipeline, PipelineExecutionResult
from src.core.step import StepExecutionResult

class PipelineRunner:
    
    def run(
        self,
        pipeline : Pipeline,
        ctx : PipelineContext
    ) -> PipelineExecutionResult:
        
        ctx.logger.info(
            "Running %s | layer %s",
            pipeline.name, pipeline.layer
        )
        
        timestamp = datetime.now().isoformat()
        start = perf_counter()
        result = []
        
        for step in pipeline.steps:
            ctx.logger.info(
                "%s | Running step %s",
                pipeline.layer, step.name
            )
            step_timestamp = datetime.now().isoformat()
            step_start = perf_counter()
            
            step_result = step.run(ctx)
            
            step_duration = round(perf_counter() - step_start, 5)

            ctx.logger.log_status(
                step_result.status,
                "%s | %s result: Status %s | Duration %ss",
                pipeline.layer, step.name, step_result.status, step_duration
            )
            
            result.append(
                StepExecutionResult(
                    name = step.name,
                    status = step_result.status,
                    duration_seconds = step_duration,
                    timestamp = step_timestamp,
                    result = step_result.result
                )
            )
            
        duration = round(perf_counter() - start, 5)
        
        status = "PASS"
        warnings = 0
        fails = 0

        for r in result:
            if r.status == "FAIL":
                fails += 1
            elif r.status == "WARNING":
                warnings += 1

        if fails > 0:
            status = "FAIL"
        elif warnings > 0:
            status = "WARNING"
        else:
            status = "PASS"
            
        ctx.logger.info("Pipeline finished: %s", pipeline.name)
        ctx.logger.log_status(
            status,
            "Overall status for %s : %s",
            pipeline.name,
            status
        )
        ctx.logger.info("Warnings: %s | Fails: %s", warnings, fails)
        ctx.logger.info("Total duration: %.5fs", duration)
        
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
            