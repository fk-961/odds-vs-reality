import pandas as pd

from src.core.framework.types import Status
from src.core.framework.step import PipelineStep, StepResult
from src.ingestion.core.context import IngestionContext
from src.core.execution.context import ExecutionContext

class FixColumns(PipelineStep):
    name = "Fix Columns"
    
    def run(
        self,
        ctx : IngestionContext,
        etx : ExecutionContext
    ) -> StepResult:
        
        # 2 kinda redundant checks
        raw_matches = ctx.get_artifact("raw_matches")
        
        if not raw_matches:
            reason = "raw table is empty in context's artifacts"
            etx.logger.error(reason)
            return StepResult(
                status = Status.FAIL,
                message = reason
            )
            
        normalized = {}
        
        for name, df in raw_matches.items():
            try:
                etx.logger.info("Fixing columns for %s", name)
                
                df = df.copy()
                if not ctx.required_cols.issubset(set(df.columns)):
                    missing_cols = ctx.required_cols.difference(set(df.columns))
                    reason = "Missing required columns"
                    etx.logger.error("%s: %s", reason, missing_cols)
                    return StepResult(
                        status = Status.FAIL,
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
                etx.logger.error("%s: %s", reason, e)
                return StepResult(
                    status = Status.FAIL,
                    message = reason,
                    error = f"{type(e).__name__}: {e}"
                )
        
        ctx.artifacts['normalized_matches'] = normalized
            
        return StepResult(
            status = Status.PASS,
            step_results = {
                "tables_processed" : len(normalized),
                "rows_processed" : sum(len(df) for df in normalized.values())
            }
        )
            