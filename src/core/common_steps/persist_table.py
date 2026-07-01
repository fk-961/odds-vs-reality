from src.core.step import PipelineStep, StepResult
from src.core.context import PipelineContext
from src.db.utils import create_table

class PersistTable(PipelineStep):
    
    def __init__(self, artifact : str, table_name : str):
        self.artifact = artifact
        self.table_name = table_name
        self.name = f"Persist table [{self.table_name}]"
    
    def run(self, ctx : PipelineContext) -> StepResult:
        create_table(
            ctx.artifacts[self.artifact],
            self.table_name,
            ctx.engine
        )
        return StepResult(
            status = "PASS",
            result = {}
        )