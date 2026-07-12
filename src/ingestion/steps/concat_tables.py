import pandas as pd

from src.core.framework.step import PipelineStep, StepResult
from src.core.execution.context import (
    PipelineContext, ExecutionContext
)
from src.core.framework.types import Status

class ConcatTables(PipelineStep):
    name = "Concatenate tables"
    
    def run(
        self,
        ctx : PipelineContext,
        etx : ExecutionContext
    ) -> StepResult:
        
        normalized_matches = ctx.get_artifact("normalized_matches")
        
        try:
            data = pd.concat(
                list(normalized_matches.values()),
                ignore_index = True
            )
            
        except Exception as e:
            message = "Could not concatenate tables"
            error = str(e)
            return StepResult(
                status = Status.FAIL,
                message = message,
                error = error
            )
            
        ctx.artifacts['matches'] = data
            
        return StepResult(
            status = Status.PASS,
            step_results = {
                "tables_concatenated" : len(normalized_matches),
                "total_rows" : int(data.shape[0]),
                "total_columns" : int(data.shape[1])
            }
        )