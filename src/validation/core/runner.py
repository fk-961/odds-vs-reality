
from datetime import datetime
from time import perf_counter

from src.validation.core.check import CheckExecutionResult
from src.validation.core.pipeline import (
    ValidationPipeline, ValidationExecutionResult
)
from src.validation.core.context import ValidationContext

class ValidationRunner:
    
    def run(
        self,
        ctx : ValidationContext,
        pipeline : ValidationPipeline
    ) -> ValidationExecutionResult:
        
        ctx.logger.info("Starting %s pipeline", pipeline.name)
        
        timestamp = datetime.now().isoformat()
        start = perf_counter()
        
        result = []
        
        for check in pipeline.checks:
            ctx.logger.info("Running %s check", check.name)
            
            check_timestamp = datetime.now().isoformat()
            check_start = perf_counter()
            
            check_result = check.run(ctx)
            
            check_duration = round(perf_counter() - check_start, 5)
            ctx.logger.log_status(
                check_result.status,
                "Status: %s | Duration %.5fs",
                check_result.status,
                check_duration
            )
            
            result.append(CheckExecutionResult(
                name = check.name,
                status = check_result.status,
                duration_seconds = check_duration,
                timestamp = check_timestamp,
                result = check_result.result
            ))
            
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
        
        
        return ValidationExecutionResult(
            name = pipeline.name,
            status = status,
            warnings = warnings,
            fails = fails,
            duration_seconds = duration,
            timestamp = timestamp,
            result = result
        )