from src.core.step import PipelineStep, StepResult
from src.transformation.core.context import TransformationContext
from src.transformation.services.build_teams import build_teams

class BuildTeams(PipelineStep):
    name = "Build teams table"
    
    def run(self, ctx : TransformationContext) -> StepResult:
        standings = ctx.artifacts["standings"]
        
        teams = build_teams(standings)
        ctx.artifacts["teams"] = teams
        return StepResult(
            status = "PASS",
            result = {}
        )