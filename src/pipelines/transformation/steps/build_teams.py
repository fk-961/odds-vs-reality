from maestro import blueprints as bp
from maestro import runtime as rt

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
            message = "standings table empty"
            etx.logger.error(message)
            
            return self.fail(msg = message)
        
        teams = build_teams(standings)
        ctx.artifacts["teams"] = teams
            
        return self.success(
            output = {
                "table_name" : "teams",
                "teams_found" : len(teams)
            }
        )