from maestro import blueprints as bp
from maestro import runtime as rt
from maestro.common.types import Status

from src.processing.transformation.build_expected_standings import (
    build_expected_standings
)

class BuildExpectedStandings(bp.PipelineStep):
    name = "Build expected_standings table"
    
    def run(
        self,
        ctx : rt.PipelineContext,
        etx : rt.ExecutionContext
    ) -> bp.StepResult:
        
        expected_points = ctx.get_artifact("expected_points")
        if expected_points.empty:
            etx.logger.error("expected_points table empty")
            return bp.StepResult(
                status = Status.FAIL,
                message = "expected_points table empty"
            )
            
        expected_standings = build_expected_standings(expected_points)
        ctx.artifacts["expected_standings"] = expected_standings
        
        return bp.StepResult(
            status = Status.PASS,
            step_results = {
                "table_name" : "expected_points",
                "rows_created" : int(expected_standings.shape[0]),
                "cols_created" : int(expected_points.shape[1])
            }
        )