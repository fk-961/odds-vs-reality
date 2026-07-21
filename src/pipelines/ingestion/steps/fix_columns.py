import pandas as pd
from maestro import blueprints as bp
from maestro import runtime as rt

class FixColumns(bp.PipelineStep):
    def __init__(self, file : str):
        self.file = file
        self.name = f"Fix {file} columns"
    
    def run(
        self,
        ctx : rt.PipelineContext,
        etx : rt.ExecutionContext
    ) -> bp.StepResult:
        
        raw_file = ctx.get_artifact(self.file)
        
        etx.logger.info("Fixing columns for %s", self.file)
        df = raw_file.copy()
        
        if not ctx.required_cols.issubset(set(df.columns)):
            missing_cols = ctx.required_cols.difference(set(df.columns))
            message = "Missing required columns"
            etx.logger.error("%s: %s", message, missing_cols)
            
            return self.fail(msg = f"Missing columns: {missing_cols}")
        
        df = df[df.columns.intersection(ctx.col_mapping.keys())]
        df = df.rename(columns = ctx.col_mapping)
        
        df['season'] = f"{self.file[3:5]}/{self.file[5:]}"
        df['league_division'] = 'L1'
        
        df['match_date'] = pd.to_datetime(
            df['match_date'], dayfirst = True
        ).dt.date
        
        ctx.artifacts[f"normalized_{self.file}"] = df
        
        return self.success()