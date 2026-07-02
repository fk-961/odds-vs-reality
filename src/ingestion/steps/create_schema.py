"""
Creates our raw table in the database with defined schema.
"""
from sqlalchemy import text

from src.core.step import PipelineStep, StepResult
from src.ingestion.core.context import IngestionContext
from src.config import ROOT_DIR

class CreateSchema(PipelineStep):
    name = "Create Schema"
    
    def run(self, ctx : IngestionContext) -> StepResult:
        
        source_schema = ctx.raw_schema.relative_to(ROOT_DIR.parent)
        if not ctx.raw_schema.exists():
            reason = f"{source_schema} does not exist"
            ctx.logger.error(reason)
            return StepResult(
                status = "FAIL",
                message = reason
            )
            
        try:
            with open(ctx.raw_schema, "r") as f:
                schema_sql = f.read()
        except Exception as e:
            reason = f"Could not read {source_schema}"
            ctx.logger.error(reason)
            return StepResult(
                status = "FAIL",
                message = reason,
                error = str(e)
            )
            
            
        try:
            with ctx.engine.begin() as conn:
                conn.execute(text(schema_sql))
        except Exception as e:
            reason = f"Could not create schema"
            ctx.logger.error(reason)
            return StepResult(
                status = "FAIL",
                message = reason,
                error = str(e)
            )
        
        ctx.logger.info("Schema successfully created")
        return StepResult(
            status = "PASS",
            result = {
                "schema_file" : str(source_schema)
            }
        )