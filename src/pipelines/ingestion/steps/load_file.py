from maestro import blueprints as bp
from maestro import runtime as rt
import pandas as pd
from pathlib import Path

class LoadFile(bp.PipelineStep):
    def __init__(self, file : Path):
        self.file = file
        self.name = f"Load {file.stem}"
        
    def run(
        self,
        ctx : rt.PipelineContext,
        etx : rt.ExecutionContext
    ) -> bp.StepResult:
        
        df = pd.read_csv(self.file)
        if df.empty:
            message = f"{self.file.stem} has no data"
            etx.logger.error(message)
            
            return self.fail(msg = message)
        
        ctx.artifacts[self.file.stem] = df
        
        return self.success(
            output = {
                "file_read" : self.file.stem,
                "rows_read" : int(df.shape[0])
            }
        )