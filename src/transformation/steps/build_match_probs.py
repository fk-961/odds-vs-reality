from src.core.step import PipelineStep, StepResult
from src.transformation.core.context import TransformationContext
from src.transformation.services.build_match_probs import build_match_probs

class BuildMatchProbs(PipelineStep):
    name = "Build Match Probabilites table"
    
    def run(self, ctx : TransformationContext) -> StepResult:
        matches = ctx.get_artifact("matches")
        
        match_probs = build_match_probs(matches)
        ctx.artifacts["match_probs"] = match_probs
        return StepResult(
            status = "PASS",
            result = {
                "table_name" : "match_probs",
                "rows_loaded" : len(match_probs)
            }
        )