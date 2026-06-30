import pandas as pd

from src.core.step import PipelineStep, StepResult
from src.ingestion.core.context import IngestionContext
from src.config import ROOT_DIR

class ExtractData(PipelineStep):
    name = "Extract Data"
    
    def run(self, ctx : IngestionContext) -> StepResult:
        data = {}
        
        files = {}
        nb_files = 0
        total_rows = 0
        
        
        source_path = ctx.source_data.relative_to(ROOT_DIR.parent)
        ctx.logger.info("Looking for data in %s", source_path)
        
        for file in ctx.source_data.glob("*.csv"):
            ctx.logger.info("CSV file found: %s", file.stem)
            
            df = pd.read_csv(file)
            data[file.stem] = df
            files[file.stem] = {
                "nb_rows" : int(df.shape[0]),
                "nb_columns" : int(df.shape[1])
            }
            
            nb_files += 1
            total_rows += int(df.shape[0])
        
        if not data:
            ctx.logger.error("No data found")
            return StepResult(
                status = "FAIL",
                result = {}
            )
            
        ctx.logger.info("%s files found", nb_files)
        ctx.artifacts['raw'] = data
        return StepResult(
            status = "PASS",
            result = {
                "files_processed" : nb_files,
                "total_rows" : total_rows,
                "files" : files
            }
        )