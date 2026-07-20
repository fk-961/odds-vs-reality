from maestro import blueprints as bp
from maestro import runtime as rt
from maestro.common.types import Status

from src.processing.analytics.build_match_metrics import build_match_metrics

class BuildMatchMetrics(bp.PipelineStep):
    name = "Build match_metrics table"
    
    def run(
        self,
        ctx : rt.PipelineContext,
        etx : rt.ExecutionContext
    ) -> bp.StepResult:
        match_probs = ctx.get_artifact("match_probs")
        
        if match_probs.empty:
            message = "match_probs table empty"
            etx.logger.error(message)
            
            return self.fail(msg = message)

            
        match_metrics = build_match_metrics(match_probs)
        ctx.artifacts["match_metrics"] = match_metrics
        
        return self.success(
            output = {
                "table_name" : "match_metrics",
                "rows_created" : int(match_metrics.shape[0]),
                "cols_created" : int(match_metrics.shape[1])
            }
        )
