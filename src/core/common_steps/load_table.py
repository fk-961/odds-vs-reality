from src.core.step import PipelineStep, StepResult
from src.core.context import PipelineContext
from src.db.utils import load_table

class LoadTable(PipelineStep):
    def __init__(self, table_name : str):
        self.name = f"Load table [{table_name}]"
        self.table_name = table_name
    
    def run(
        self,
        ctx : PipelineContext,
    ) -> StepResult:
        table = load_table(self.table_name, ctx.engine)
        
        if table.empty:
            return StepResult(
                status = "FAIL",
                result = {}
            )
            
        ctx.artifacts[self.table_name] = table
        return StepResult(
            status = "PASS",
            result = {
                "nb_rows" : table.shape[0],
                "nb_columns" : table.shape[1]
            }
        )