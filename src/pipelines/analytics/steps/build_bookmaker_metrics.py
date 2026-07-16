from src.core.framework.step import (
    PipelineStep, StepResult
)
from src.core.execution.context import (
    PipelineContext, ExecutionContext
)
from src.core.framework.types import Status
from src.processing.analytics.build_bookmaker_metrics import (
    build_bookmaker_metrics
)

class BuildBookmakerMetrics(PipelineStep):
    name = "Build bookmaker_metrics table"
    
    def run(
        self,
        ctx : PipelineContext,
        etx : PipelineStep
    ) -> StepResult:
        match_metrics = ctx.get_artifact("match_metrics")
        if match_metrics.empty:
            etx.logger.error("match_metrics table empty")
            return StepResult(
                status = Status.FAIL,
                message = "match_metrics table empty"
            )
            
        bookmaker_metrics = build_bookmaker_metrics(match_metrics)
        ctx.artifacts["bookmaker_metrics"] = bookmaker_metrics
        return StepResult(
            status = Status.PASS,
            step_results = {
                "table_name" : "bookmaker_metrics",
                "rows_created" : int(bookmaker_metrics.shape[0]),
                "cols_created" : int(bookmaker_metrics.shape[1])
            }
        )