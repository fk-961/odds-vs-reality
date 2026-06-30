from src.core.step import PipelineStep, StepResult
from src.transformation.core.context import TransformationContext
from src.db.utils import load_table

class LoadMatches(PipelineStep):
    name = "Load matches table"
    
    def run(self, ctx : TransformationContext) -> StepResult:
        matches = load_table("matches", ctx.engine)
        
        if matches.empty:
            return StepResult(
                status = "FAIL",
                result = {}
            )
            
        ctx.artifacts["matches"] = matches
        return StepResult(
            status = "PASS",
            result = {
                "nb_rows" : matches.shape[0],
                "nb_columns" : matches.shape[1]
            }
        )