from src.core.step import PipelineStep, StepResult
from src.analytics.core.context import AnalyticsContext
from src.analytics.services.build_match_metrics import build_match_metrics

class BuildMatchMetrics(PipelineStep):
    name = "Build match_metrics"
    
    def run(self, ctx : AnalyticsContext) -> StepResult:
        match_probs = ctx.artifacts["match_probs"]
        
        match_metrics = build_match_metrics(match_probs)
        ctx.artifacts["match_metrics"] = match_metrics
        return StepResult(
            status = "PASS",
            result = {}
        )