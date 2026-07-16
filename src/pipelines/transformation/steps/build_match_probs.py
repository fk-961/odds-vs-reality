from maestro import blueprints as bp
from maestro import runtime as rt
from maestro.common.types import Status

from src.processing.transformation.build_match_probs import (
    build_match_probs
)

class BuildMatchProbs(bp.PipelineStep):
    name = "Build Table match_probs"
    
    def run(
        self,
        ctx : rt.PipelineContext,
        etx : rt.ExecutionContext
    ) -> bp.StepResult:
        
        matches = ctx.get_artifact("matches")
        
        if matches.empty:
            etx.logger.error("Matches table empty")
            return bp.StepResult(
                status = Status.FAIL,
                message = "matches table empty"
            )
            
        match_probs = build_match_probs(matches)
        ctx.artifacts["match_probs"] = match_probs
        
        return bp.StepResult(
            status = Status.PASS,
            step_results = {
                "table_name" : "match_probs",
                "rows_created" : int(match_probs.shape[0]),
                "cols_created" : int(match_probs.shape[1])
            }
        )