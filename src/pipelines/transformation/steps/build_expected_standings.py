from maestro import blueprints as bp
from maestro import runtime as rt

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
            message = "expected_points table empty"
            etx.logger.error(message)
            
            return self.fail(msg = message)
            
        expected_standings = build_expected_standings(expected_points)
        ctx.artifacts["expected_standings"] = expected_standings
        
        return self.success(
            output = {
                "table_name" : "expected_standings",
                "rows_created" : int(expected_standings.shape[0]),
                "cols_created" : int(expected_standings.shape[1])
            }
        )