"""
Creates our raw table in the database with defined schema.
"""
from sqlalchemy import text
from maestro import blueprints as bp
from maestro import runtime as rt

from src.config import ROOT_DIR

class CreateSchema(bp.PipelineStep):
    name = "Create Schema"
    
    def run(
        self,
        ctx : rt.PipelineContext,
        etx : rt.ExecutionContext
    ) -> bp.StepResult:
        
        source_schema = ctx.raw_schema.relative_to(ROOT_DIR.parent)
        if not ctx.raw_schema.exists():
            reason = f"{source_schema} does not exist"
            etx.logger.error(reason)
            return self.fail(
                msg = reason
            )
            
        with open(ctx.raw_schema, "r") as f:
            schema_sql = f.read()
            
            
        with ctx.engine.begin() as conn:
            conn.execute(text(schema_sql))
            
        etx.logger.info("Schema successfully created")
        return self.success(
            output = {
                "schema_file" : str(source_schema)
            }
        )
