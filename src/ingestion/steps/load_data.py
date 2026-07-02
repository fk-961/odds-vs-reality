import pandas as pd

from src.core.step import PipelineStep, StepResult
from src.ingestion.core.context import IngestionContext

class LoadData(PipelineStep):
    name = "Load Data"
    
    def run(self, ctx : IngestionContext) -> StepResult:
        
        normalized_matches = ctx.get_artifact("normalized")
            
        try:
            data = pd.concat(
                list(normalized_matches.values()),
                ignore_index = True
            )
        except Exception as e:
            reason = "Could not concatenate normalized data"
            ctx.logger.error("%s: %s", reason, e)
            return StepResult(
                status = "FAIL",
                message = reason,
                error = str(e)
            )
        
        try:
            data.to_sql(
                "matches",
                ctx.engine,
                if_exists = "append",
                index = False
            )
        except Exception as e:
            reason = "Could not write data to database"
            ctx.logger.error("%s: %s", reason, e)
            return StepResult(
                status = "FAIL",
                message = reason,
                error = str(e)
            )
        
        return StepResult(
            status = "PASS",
            result = {
                "table_name" : "matches",
                "rows_loaded" : len(data),
                "columns_loaded" : int(data.shape[1])
            }
        )