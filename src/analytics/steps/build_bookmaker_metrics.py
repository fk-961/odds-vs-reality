from src.core.step import PipelineStep, StepResult
from src.analytics.core.context import AnalyticsContext
from src.analytics.services.build_bookmaker_metrics import build_bookmaker_metrics

class BuildBookmakerMetrics(PipelineStep):
    name = "Build bookmaker_metrics"
    
    def run(self, ctx : AnalyticsContext) -> StepResult:
        match_metrics = ctx.get_artifact("match_metrics")
        
        bookmaker_metrics = build_bookmaker_metrics(match_metrics)
        ctx.artifacts["bookmaker_metrics"] = bookmaker_metrics
        
        return StepResult(
            status = "PASS",
            result = {
                "table_name" : "bookmaker_metrics",
                "rows_loaded" : len(bookmaker_metrics)
            }
        )