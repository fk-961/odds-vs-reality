"""
Creates our raw table in the database with defined schema.
"""
from pathlib import Path
from sqlalchemy import text
from sqlalchemy.engine import Engine

from src.ingestion.core.step import (
    IngestionStep, StepResult
)
from src.ingestion.core.context import IngestionContext

class CreateSchema(IngestionStep):
    name = "Create Schema"
    
    def run(self, ctx : IngestionContext) -> StepResult:
        with open(ctx.raw_schema, "r") as f:
            schema_sql = f.read()
            
        with ctx.engine.begin() as conn:
            conn.execute(text(schema_sql))
            
        return StepResult(
            status = "PASS",
            result = []
        )