from maestro import blueprints as bp
from maestro import runtime as rt

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
            message = "matches table empty"
            etx.logger.error(message)
            
            return self.fail(msg = message)
            
        match_probs = build_match_probs(matches)
        ctx.artifacts["match_probs"] = match_probs
        
        return self.success(
            output = {
                "table_name" : "match_probs",
                "rows_created" : int(match_probs.shape[0]),
                "cols_created" : int(match_probs.shape[1])
            }
        )