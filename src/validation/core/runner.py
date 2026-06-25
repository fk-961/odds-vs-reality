
from datetime import datetime
from time import perf_counter
from sqlalchemy.engine import Engine

from src.validation.core.check import CheckExecutionResult
from src.validation.core.pipeline import (
    ValidationPipeline, ValidationExecutionResult
)

class ValidationRunner:
    
    def run(
        self,
        engine : Engine,
        pipeline : ValidationPipeline
    ) -> ValidationExecutionResult:
        
        print("\n" + "=" * 50)
        print(f"Starting validation pipeline: {pipeline.name}")
        print("=" * 50)
        
        timestamp = datetime.now().isoformat()
        start = perf_counter()
        
        result = []
        
        for check in pipeline.checks:
            print(f" Running: {check.name}")
            
            check_timestamp = datetime.now().isoformat()
            check_start = perf_counter()
            
            check_result = check.run(engine)
            
            check_duration = round(perf_counter() - check_start, 5)
            print(f"→ Status: {check_result.status} | Duration: {check_duration}s")
            
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
            
        print("\n" + "-" * 50)
        print(f"Pipeline finished: {pipeline.name}")
        print(f"Status: {status}")
        print(f"Warnings: {warnings} | Fails: {fails}")
        print(f"Total duration: {duration}s")
        print("-" * 50 + "\n")
        
        
        return ValidationExecutionResult(
            name = pipeline.name,
            status = status,
            warnings = warnings,
            fails = fails,
            duration_seconds = duration,
            timestamp = timestamp,
            result = result
        )