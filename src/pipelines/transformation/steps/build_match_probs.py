from src.core.framework.step import (
    PipelineStep, StepResult
)
from src.core.execution.context import (
    PipelineContext, ExecutionContext
)
from src.core.framework.types import Status
from src.processing.transformation.build_match_probs import (
    build_match_probs
)

class BuildMatchProbs(PipelineStep):
    name = "Build Table match_probs"
    
    def run(
        self,
        ctx : PipelineContext,
        etx : ExecutionContext
    ) -> StepResult:
        
        matches = ctx.get_artifact("matches")
        
        if matches.empty:
            etx.logger.error("Matches table empty")
            return StepResult(
                status = Status.FAIL,
                message = "matches table empty"
            )
            
        match_probs = build_match_probs(matches)
        ctx.artifacts["match_probs"] = match_probs
        
        return StepResult(
            status = Status.PASS,
            step_results = {
                "table_name" : "match_probs",
                "rows_created" : int(match_probs.shape[0]),
                "cols_created" : int(match_probs.shape[1])
            }
        )