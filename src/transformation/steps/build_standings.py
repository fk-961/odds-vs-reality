from src.core.framework.step import (
    PipelineStep, StepResult
)
from src.core.execution.context import (
    PipelineContext, ExecutionContext
)
from src.core.framework.types import Status
from src.processing.transformation.build_standings import (
    build_standings
)

class BuildStandings(PipelineStep):
    name = "Build table standings"
    
    def run(
        self,
        ctx : PipelineContext,
        etx : ExecutionContext
    ) -> StepResult:
        
        matches = ctx.get_artifact("matches")
        
        if matches.empty:
            etx.logger.error("Matches Table empty")
            return StepResult(
                status = Status.FAIL,
                message = "Table empty"
            )
        
        standings = build_standings(matches)
        ctx.artifacts["standings"] = standings
            
        return StepResult(
            status = Status.PASS,
            step_results = {
                "table_name" : "standings",
                "rows_created" : int(standings.shape[0]),
                "cols_created" : int(standings.shape[1])
            }
        )