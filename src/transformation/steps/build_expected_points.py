from src.core.framework.step import (
    PipelineStep, StepResult
)
from src.core.execution.context import (
    PipelineContext, ExecutionContext
)
from src.core.framework.types import Status
from src.processing.transformation.build_expected_points import (
    build_expected_points
)

class BuildExpectedPoints(PipelineStep):
    name = "Build expected_points table"
    
    def run(
        self,
        ctx : PipelineContext,
        etx : ExecutionContext
    ) -> StepResult:
        
        match_probs = ctx.get_artifact("match_probs")
        if match_probs.empty:
            etx.logger.error("match_probs table empty")
            return StepResult(
                status = Status.FAIL,
                message = "match_probs empty"
            )
            
        expected_points = build_expected_points(match_probs)
        ctx.artifacts["expected_points"] = expected_points
        
        return StepResult(
            status = Status.PASS,
            step_results = {
                "table_name" : "expected_points",
                "rows_created" : int(expected_points.shape[0]),
                "cols_created" : int(expected_points.shape[1])
            }
        )