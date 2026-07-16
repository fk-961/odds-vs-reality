from maestro import blueprints as bp
from maestro import runtime as rt
from maestro.common.types import Status

from src.processing.transformation.build_standings import (
    build_standings
)

class BuildStandings(bp.PipelineStep):
    name = "Build table standings"
    
    def run(
        self,
        ctx : rt.PipelineContext,
        etx : rt.ExecutionContext
    ) -> bp.StepResult:
        
        matches = ctx.get_artifact("matches")
        
        if matches.empty:
            etx.logger.error("Matches Table empty")
            return bp.StepResult(
                status = Status.FAIL,
                message = "Table empty"
            )
        
        standings = build_standings(matches)
        ctx.artifacts["standings"] = standings
            
        return bp.StepResult(
            status = Status.PASS,
            step_results = {
                "table_name" : "standings",
                "rows_created" : int(standings.shape[0]),
                "cols_created" : int(standings.shape[1])
            }
        )