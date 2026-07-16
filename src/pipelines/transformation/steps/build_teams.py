from maestro import blueprints as bp
from maestro import runtime as rt
from maestro.common.types import Status

from src.processing.transformation.build_teams import (
    build_teams
)

class BuildTeams(bp.PipelineStep):
    name = "Build table teams"
    
    def run(
        self,
        ctx : rt.PipelineContext,
        etx : rt.ExecutionContext
    ) -> bp.StepResult:
        
        standings = ctx.get_artifact("standings")
        
        if standings.empty:
            etx.logger.error("Standings Table empty")
            return bp.StepResult(
                status = Status.FAIL,
                message = "Standings Table empty"
            )
        
        teams = build_teams(standings)
        ctx.artifacts["teams"] = teams
            
        return bp.StepResult(
            status = Status.PASS,
            step_results = {
                "table_name" : "teams",
                "teams_found" : len(teams)
            }
        )