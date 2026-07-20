"""
Loads a table from our database and add it to runtime artifacts.
"""

from maestro import blueprints as bp
from maestro import runtime as rt

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
            message = f"{self.table_name} table empty"
            etx.logger.error(message)
            return self.fail(
                msg = message
            )
            
        ctx.artifacts[self.table_name] = table
        return self.success(
            output = {
                "table_name" : self.table_name,
                "nb_rows" : int(table.shape[0]),
                "nb_columns" : int(table.shape[1])
            }
        )
    