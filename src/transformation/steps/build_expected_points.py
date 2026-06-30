from src.core.step import PipelineStep, StepResult
from src.transformation.core.context import TransformationContext
from src.transformation.services.build_expected_points import build_expected_points

class BuildExpectedPoints(PipelineStep):
    name = "Build expected_points table"
    
    def run(self, ctx : TransformationContext) -> StepResult:
        match_probs = ctx.artifacts["match_probs"]
        
        expected_points = build_expected_points(match_probs)
        ctx.artifacts["expected_points"] = expected_points
        return StepResult(
            status = "PASS",
            result = {}
        )