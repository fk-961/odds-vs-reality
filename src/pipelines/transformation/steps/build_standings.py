from maestro import blueprints as bp
from maestro import runtime as rt

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
            message = "matches table empty"
            etx.logger.error(message)
            
            return self.fail(msg = message)
        
        standings = build_standings(matches)
        ctx.artifacts["standings"] = standings
            
        return self.success(
            output = {
                "table_name" : "standings",
                "rows_created" : int(standings.shape[0]),
                "cols_created" : int(standings.shape[1])
            }
        )