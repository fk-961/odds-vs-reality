from sqlalchemy import text
from maestro import blueprints as bp
from maestro import runtime as rt
from maestro.common.types import Status

from src.db.common.utils import create_table

class PersistTable(bp.PipelineStep):
    
    def __init__(self, artifact : str, table_name : str):
        self.artifact = artifact
        self.table_name = table_name
        self.name = f"Persist table [{self.table_name}]"
    
    def run(
        self,
        ctx : rt.PipelineContext,
        etx : rt.ExecutionContext
    ) -> bp.StepResult:
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
        return bp.StepResult(
            status = Status.PASS,
        )