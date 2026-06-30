from src.core.step import PipelineStep, StepResult
from src.transformation.core.context import TransformationContext
from src.db.utils import create_table

class PersistTable(PipelineStep):
    name = "Persist data"
    
    def __init__(self, artifact : str, table_name : str):
        self.artifact = artifact
        self.table_name = table_name
    
    def run(self, ctx : TransformationContext) -> StepResult:
        create_table(
            ctx.artifacts[self.artifact],
            self.table_name,
            ctx.engine
        )
        return StepResult(
            status = "PASS",
            result = {}
        )