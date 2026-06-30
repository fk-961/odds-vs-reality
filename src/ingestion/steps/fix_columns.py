import pandas as pd

from src.ingestion.core.step import IngestionStep, StepResult
from src.ingestion.core.context import IngestionContext

class FixColumns(IngestionStep):
    name = "Fix Columns"
    
    def run(self, ctx : IngestionContext) -> StepResult:
        normalized = {}
        
        for name, df in ctx.artifacts['raw'].items():
            ctx.logger.info("Fixing columns for %s", name)
            
            df = df.copy()
            
            # get schema columns
            df = df[df.columns.intersection(ctx.col_mapping.keys())]
            df = df.rename(columns = ctx.col_mapping)
            
            # add season and league division cols
            df['season'] = f"{name[3:5]}/{name[5:]}"
            df['league_division'] = "L1"
            
            # convert match date
            df['match_date'] = pd.to_datetime(
                df['match_date'], dayfirst = True
            ).dt.date
            
            normalized[name] = df
        
        ctx.artifacts['normalized'] = normalized
            
        return StepResult(
            status = "PASS",
            result = {}
        )
            