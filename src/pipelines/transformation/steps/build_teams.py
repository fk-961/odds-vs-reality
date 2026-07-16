from src.core.framework.step import (
    PipelineStep, StepResult
)
from src.core.execution.context import (
    PipelineContext, ExecutionContext
)
from src.core.framework.types import Status
from src.processing.transformation.build_teams import (
    build_teams
)

class BuildTeams(PipelineStep):
    name = "Build table teams"
    
    def run(
        self,
        ctx : PipelineContext,
        etx : ExecutionContext
    ) -> StepResult:
        
        standings = ctx.get_artifact("standings")
        
        if standings.empty:
            etx.logger.error("Standings Table empty")
            return StepResult(
                status = Status.FAIL,
                message = "Standings Table empty"
            )
        
        teams = build_teams(standings)
        ctx.artifacts["teams"] = teams
            
        return StepResult(
            status = Status.PASS,
            step_results = {
                "table_name" : "teams",
                "teams_found" : len(teams)
            }
        )