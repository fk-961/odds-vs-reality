from src.core.step import PipelineStep, StepResult
from src.transformation.core.context import TransformationContext
from src.transformation.services.build_expected_standings import build_expected_standings

class BuildExpectedStandings(PipelineStep):
    name = "Build expected_standings table"
    
    def run(self, ctx : TransformationContext) -> StepResult:
        expected_points = ctx.get_artifact("expected_points")
        
        expected_standings = build_expected_standings(expected_points)
        ctx.artifacts["expected_standings"] = expected_standings
        return StepResult(
            status = "PASS",
            result = {}
        )