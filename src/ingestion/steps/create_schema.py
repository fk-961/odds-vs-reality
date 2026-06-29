"""
Creates our raw table in the database with defined schema.
"""
from pathlib import Path
from sqlalchemy.engine import Engine

from src.ingestion.core.step import (
    IngestionStep, StepResult
)

class CreateSchema(IngestionStep):
    name = "Create Schema"
    
    def __init__(self, schema : Path, engine : Engine):
        self.schema = schema
        self.engine = engine
        