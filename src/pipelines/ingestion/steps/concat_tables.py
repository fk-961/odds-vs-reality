import pandas as pd
from maestro import blueprints as bp
from maestro import runtime as rt

class ConcatTables(bp.PipelineStep):
    name = "Concatenate tables"
    
    def run(
        self,
        ctx : rt.PipelineContext,
        etx : rt.ExecutionContext
    ) -> bp.StepResult:
        
        normalized_matches = ctx.get_artifact("normalized_matches")
        if not normalized_matches:
            message = "normalized_matches artifact empty"
            etx.logger.error(message)
            return self.fail(
                msg = message
            )
            
        data = pd.concat(
            list(normalized_matches.values()),
            ignore_index = True
        )
            
        ctx.artifacts['matches'] = data
        
        return self.success(
            output = {
                "tables_concatenated" : len(normalized_matches),
                "total_rows" : int(data.shape[0]),
                "total_columns" : int(data.shape[1])
            }
        )
        