"""
Creates our raw table in the database with defined schema.
"""
from sqlalchemy import text

from src.core.framework.types import Status
from src.core.framework.step import PipelineStep, StepResult
from src.ingestion.core.context import IngestionContext
from src.core.execution.context import ExecutionContext
from src.config import ROOT_DIR

class CreateSchema(PipelineStep):
    name = "Create Schema"
    
    def run(
        self,
        ctx : IngestionContext,
        etx : ExecutionContext
    ) -> StepResult:
        
        source_schema = ctx.raw_schema.relative_to(ROOT_DIR.parent)
        if not ctx.raw_schema.exists():
            reason = f"{source_schema} does not exist"
            etx.logger.error(reason)
            return StepResult(
                status = Status.FAIL,
                message = reason
            )
            
        try:
            with open(ctx.raw_schema, "r") as f:
                schema_sql = f.read()
        except Exception as e:
            reason = f"Could not read {source_schema}"
            etx.logger.error(reason)
            return StepResult(
                status = Status.FAIL,
                message = reason,
                error = str(e)
            )
            
            
        try:
            with ctx.engine.begin() as conn:
                conn.execute(text(schema_sql))
        except Exception as e:
            reason = f"Could not create schema"
            etx.logger.error(reason)
            return StepResult(
                status = Status.FAIL,
                message = reason,
                error = str(e)
            )
        
        etx.logger.info("Schema successfully created")
        return StepResult(
            status = Status.PASS,
            step_results = {
                "schema_file" : str(source_schema)
            }
        )