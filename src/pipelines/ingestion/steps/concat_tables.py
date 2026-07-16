import pandas as pd
from maestro import blueprints as bp
from maestro import runtime as rt
from maestro.common.types import Status

class ConcatTables(bp.PipelineStep):
    name = "Concatenate tables"
    
    def run(
        self,
        ctx : rt.PipelineContext,
        etx : rt.ExecutionContext
    ) -> bp.StepResult:
        
        normalized_matches = ctx.get_artifact("normalized_matches")
        
        try:
            data = pd.concat(
                list(normalized_matches.values()),
                ignore_index = True
            )
            
        except Exception as e:
            message = "Could not concatenate tables"
            error = f"{type(e).__name__}: {e}"
            return bp.StepResult(
                status = Status.FAIL,
                message = message,
                error = error
            )
            
        ctx.artifacts['matches'] = data
            
        return bp.StepResult(
            status = Status.PASS,
            step_results = {
                "tables_concatenated" : len(normalized_matches),
                "total_rows" : int(data.shape[0]),
                "total_columns" : int(data.shape[1])
            }
        )