import pandas as pd

from src.core.step import PipelineStep, StepResult
from src.ingestion.core.context import IngestionContext

class LoadData(PipelineStep):
    name = "Load Data"
    
    def run(self, ctx : IngestionContext) -> StepResult:
        
        data = pd.concat(
            list(ctx.artifacts['normalized'].values()),
            ignore_index = True
        )
        
        data.to_sql(
            "matches",
            ctx.engine,
            if_exists = "append",
            index = False
        )
        
        return StepResult(
            status = "PASS",
            result = {}
        )