import pandas as pd
from maestro import blueprints as bp
from maestro import runtime as rt
from maestro.common.types import Status

from src.config import ROOT_DIR

class ExtractData(bp.PipelineStep):
    name = "Extract Data"
    
    def run(
        self,
        ctx : rt.PipelineContext,
        etx : rt.ExecutionContext
    ) -> bp.StepResult:
        data = {}
        
        files = {}
        nb_files = 0
        total_rows = 0
        
        source_path = ctx.source_data.relative_to(ROOT_DIR.parent)
        
        if not ctx.source_data.exists():
            reason = f"{source_path} does not exist"
            etx.logger.error(reason)
            return bp.StepResult(
                status = Status.FAIL,
                message = reason
            )
        
        etx.logger.info("Looking for data in %s", source_path)
        
        csv_files = list(ctx.source_data.glob("*.csv"))
        if not csv_files:
            reason = f"No files found in {source_path}"
            etx.logger.error(reason)
            return bp.StepResult(
                status = Status.FAIL,
                message = reason
            )
            
        for file in csv_files:
            etx.logger.info("CSV file found: %s", file.stem)
            
            try:
                df = pd.read_csv(file)
            except Exception as e :
                reason = f"failed to read {file.stem}"
                etx.logger.error(reason)
                return bp.StepResult(
                    status = Status.FAIL,
                    message = reason,
                    error = f"{type(e).__name__}: {e}"
                )
            
            data[file.stem] = df
            files[file.stem] = {
                "nb_rows" : int(df.shape[0]),
                "nb_columns" : int(df.shape[1])
            }
            
            nb_files += 1
            total_rows += int(df.shape[0])
            
        etx.logger.info("%s files found, total_rows = %s", nb_files, total_rows)
        ctx.artifacts['raw_matches'] = data
        return bp.StepResult(
            status = Status.PASS,
            step_results = {
                "files_processed" : nb_files,
                "total_rows" : total_rows,
                "files" : files
            }
        )