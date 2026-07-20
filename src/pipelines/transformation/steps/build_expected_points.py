from maestro import blueprints as bp
from maestro import runtime as rt

from src.processing.transformation.build_expected_points import (
    build_expected_points
)

class BuildExpectedPoints(bp.PipelineStep):
    name = "Build expected_points table"
    
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
            
        expected_points = build_expected_points(match_probs)
        ctx.artifacts["expected_points"] = expected_points
        
        return self.success(
            output = {
                "table_name" : "expected_points",
                "rows_created" : int(expected_points.shape[0]),
                "cols_created" : int(expected_points.shape[1])
            }
        )
