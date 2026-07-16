"""
Loads a table from our database and add it to runtime artifacts.
"""

from .._core.blueprints.step import PipelineStep, StepResult
from .._core.runtime.context import (
    PipelineContext, ExecutionContext
)
from src.db.utils import load_table
from .._core.blueprints.types import Status

class LoadTable(PipelineStep):
    def __init__(self, table_name : str):
        self.name = f"Load table [{table_name}]"
        self.table_name = table_name
    
    def run(
        self,
        ctx : PipelineContext,
        etx : ExecutionContext
    ) -> StepResult:
        table = load_table(self.table_name, ctx.engine)
        
        if table.empty:
            etx.logger.error("Table empty")
            return StepResult(
                status = Status.FAIL,
                message = "Table empty"
            )
            
        ctx.artifacts[self.table_name] = table
        return StepResult(
            status = Status.PASS,
            step_results = {
                "nb_rows" : table.shape[0],
                "nb_columns" : table.shape[1]
            }
        )