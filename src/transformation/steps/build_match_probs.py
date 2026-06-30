from src.core.step import PipelineStep, StepResult
from src.transformation.core.context import TransformationContext
from src.transformation.services.build_match_probs import build_match_probs

class BuildMatchProbs(PipelineStep):
    name = "Build Match Probabilites table"
    
    def run(self, ctx : TransformationContext) -> StepResult:
        matches = ctx.artifacts["matches"]
        
        match_probs = build_match_probs(matches)
        ctx.artifacts["match_probs"] = match_probs
        return StepResult(
            status = "PASS",
            result = {}
        )