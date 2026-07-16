"""
Loads a table from our database and add it to runtime artifacts.
"""

from maestro import blueprints as bp
from maestro import runtime as rt
from maestro.common.types import Status

from src.db.common.utils import load_table

class LoadTable(bp.PipelineStep):
    def __init__(self, table_name : str):
        self.name = f"Load table [{table_name}]"
        self.table_name = table_name
    
    def run(
        self,
        ctx : rt.PipelineContext,
        etx : rt.ExecutionContext
    ) -> bp.StepResult:
        table = load_table(self.table_name, ctx.engine)
        
        if table.empty:
            etx.logger.error("Table empty")
            return bp.StepResult(
                status = Status.FAIL,
                message = "Table empty"
            )
            
        ctx.artifacts[self.table_name] = table
        return bp.StepResult(
            status = Status.PASS,
            step_results = {
                "nb_rows" : table.shape[0],
                "nb_columns" : table.shape[1]
            }
        )