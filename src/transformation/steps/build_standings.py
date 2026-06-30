from src.core.step import PipelineStep, StepResult
from src.transformation.core.context import TransformationContext
from src.transformation.services.build_standings import build_standings

class BuildStandings(PipelineStep):
    name = "Build standings table"
    
    def run(self, ctx : TransformationContext) -> StepResult:
        matches = ctx.artifacts["matches"]
        
        standings = build_standings(matches)
        ctx.artifacts["standings"] = standings
        
        return StepResult(
            status = "PASS",
            result = {}
        )