from sqlalchemy import text

from .._core.blueprints.step import PipelineStep, StepResult
from .._core.execution.context import (
    PipelineContext, ExecutionContext
)
from .._core.blueprints.types import Status
from src.db.utils import create_table

class PersistTable(PipelineStep):
    
    def __init__(self, artifact : str, table_name : str):
        self.artifact = artifact
        self.table_name = table_name
        self.name = f"Persist table [{self.table_name}]"
    
    def run(
        self,
        ctx : PipelineContext,
        etx : ExecutionContext
    ) -> StepResult:
        etx.logger.info(
            "Persisting table %s", self.table_name
        )
        
        with ctx.engine.begin() as conn:
            conn.execute(
                text(f"TRUNCATE TABLE {self.table_name} RESTART IDENTITY;")
            )
        etx.logger.info(
            "%s truncated", self.table_name
        )
        
        create_table(
            ctx.artifacts[self.artifact],
            self.table_name,
            ctx.engine
        )
        return StepResult(
            status = Status.PASS,
        )