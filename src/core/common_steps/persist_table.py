from src.core.framework.step import PipelineStep, StepResult
from src.core.execution.context import (
    PipelineContext, ExecutionContext
)
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
        create_table(
            ctx.artifacts[self.artifact],
            self.table_name,
            ctx.engine
        )
        return StepResult(
            status = "PASS",
            result = {}
        )