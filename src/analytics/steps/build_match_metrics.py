from src.core.framework.step import (
    PipelineStep, StepResult
)
from src.core.execution.context import (
    PipelineContext, ExecutionContext
)
from src.core.framework.types import Status
from src.processing.analytics.build_match_metrics import build_match_metrics

class BuildMatchMetrics(PipelineStep):
    name = "Build match_metrics table"
    
    def run(
        self,
        ctx : PipelineContext,
        etx : ExecutionContext
    ) -> StepResult:
        match_probs = ctx.get_artifact("match_probs")
        
        if match_probs.empty:
            message = "match_probs table empty"
            etx.logger.error(message)
            return StepResult(
                status = Status.FAIL,
                message = message
            )
            
        match_metrics = build_match_metrics(match_probs)
        ctx.artifacts["match_metrics"] = match_metrics
        return StepResult(
            status = Status.PASS,
            step_results = {
                "table_name" : "match_metrics",
                "rows_created" : int(match_metrics.shape[0]),
                "cols_created" : int(match_metrics.shape[1])
            }
        )