import pandas as pd
from maestro import blueprints as bp
from maestro import runtime as rt

class FixColumns(bp.PipelineStep):
    name = "Fix Columns"
    
    def run(
        self,
        ctx : rt.PipelineContext,
        etx : rt.ExecutionContext
    ) -> bp.StepResult:
        
        # 2 kinda redundant checks
        raw_matches = ctx.get_artifact("raw_matches")
        
        if not raw_matches:
            reason = "raw table is empty in context's artifacts"
            etx.logger.error(reason)
            
            return self.fail(msg = reason)
            
        normalized = {}
        
        for name, df in raw_matches.items():
            etx.logger.info("Fixing columns for %s", name)
                
            df = df.copy()
            if not ctx.required_cols.issubset(set(df.columns)):
                missing_cols = ctx.required_cols.difference(set(df.columns))
                reason = "Missing required columns"
                etx.logger.error("%s: %s", reason, missing_cols)
                
                return self.fail(
                    msg = f"Missing columns: {missing_cols}"
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
            
        ctx.artifacts['normalized_matches'] = normalized
            
        return self.success(
            output = {
                "tables_processed" : len(normalized),
                "rows_processed" : sum(len(df) for df in normalized.values())
            }
        )

            