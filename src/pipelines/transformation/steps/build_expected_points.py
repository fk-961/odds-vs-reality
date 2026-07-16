from maestro import blueprints as bp
from maestro import runtime as rt
from maestro.common.types import Status

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
            etx.logger.error("match_probs table empty")
            return bp.StepResult(
                status = Status.FAIL,
                message = "match_probs empty"
            )
            
        expected_points = build_expected_points(match_probs)
        ctx.artifacts["expected_points"] = expected_points
        
        return bp.StepResult(
            status = Status.PASS,
            step_results = {
                "table_name" : "expected_points",
                "rows_created" : int(expected_points.shape[0]),
                "cols_created" : int(expected_points.shape[1])
            }
        )