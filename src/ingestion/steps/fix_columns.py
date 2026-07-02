import pandas as pd

from src.core.step import PipelineStep, StepResult
from src.ingestion.core.context import IngestionContext

class FixColumns(PipelineStep):
    name = "Fix Columns"
    
    def run(self, ctx : IngestionContext) -> StepResult:
        
        # 2 kinda redundant checks
        raw_matches = ctx.get_artifact("raw")
        
        if not raw_matches:
            reason = "raw table is empty in context's artifacts"
            ctx.logger.error(reason)
            return StepResult(
                status = "FAIL",
                result = {"reason" : reason}
            )
            
        normalized = {}
        
        for name, df in raw_matches.items():
            try:
                ctx.logger.info("Fixing columns for %s", name)
                
                df = df.copy()
                if not ctx.required_cols.issubset(set(df.columns)):
                    missing_cols = ctx.required_cols.difference(set(df.columns))
                    reason = "Missing required columns"
                    ctx.logger.error("%s: %s", reason, missing_cols)
                    return StepResult(
                        status = "FAIL",
                        message = reason,
                        error = f"missing_cols = {missing_cols}"
                    )
                
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
            
            except Exception as e:
                reason = f"Could not fix columns for {name}"
                ctx.logger.error("%s: %s", reason, e)
                return StepResult(
                    status = "FAIL",
                    message = reason,
                    error = str(e)
                )
        
        ctx.artifacts['normalized'] = normalized
            
        return StepResult(
            status = "PASS",
            result = {
                "tables_processed" : len(normalized),
                "rows_processed" : sum(len(df) for df in normalized.values())
            }
        )
            