from src.ingestion.core.pipeline import IngestionPipeline
from src.ingestion.steps.create_schema import CreateSchema
from src.ingestion.steps.extract_data import ExtractData
from src.ingestion.steps.fix_columns import FixColumns
from src.ingestion.steps.load_data import LoadData
from src.ingestion.core.runner import IngestionRunner
from src.ingestion.core.context import IngestionContext
from src.db.engine import engine
from src.core.logger import PipelineLogger
import logging
from src.config import (
    DB_SCHEMA, RAW_LIGUE1_DIR
)
from src.mappings import col_mapping
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s"
)

if __name__ == "__main__":
    ingestion_steps = [
        CreateSchema(),
        ExtractData(),
        FixColumns(),
        LoadData()
    ]
    
    ingestion_pipeline = IngestionPipeline(
        "ingestion", ingestion_steps
    )
    
    ingestion_context = IngestionContext(
        engine,
        PipelineLogger(logging.getLogger("ingestion")),
        DB_SCHEMA,
        RAW_LIGUE1_DIR,
        col_mapping
    )
    
    runner = IngestionRunner()
    results = runner.run(
        ingestion_pipeline, ingestion_context
    )
    
    