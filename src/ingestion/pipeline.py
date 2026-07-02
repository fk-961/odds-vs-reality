import logging
from src.core.logger import PipelineLogger
from src.core.pipeline import Pipeline

from src.ingestion.core.context import IngestionContext

from src.ingestion.steps.create_schema import CreateSchema
from src.ingestion.steps.extract_data import ExtractData
from src.ingestion.steps.fix_columns import FixColumns
from src.ingestion.steps.load_data import LoadData

from src.config import (
    INGESTION_SNAPSHOT,
    INGESTION_LOGS,
    DB_SCHEMA,
    RAW_LIGUE1_DIR
)
from src.db.engine import engine
from src.mappings import col_mapping, required_cols

ingestion_steps = [
    CreateSchema(),
    ExtractData(),
    FixColumns(),
    LoadData()
]

ingestion_pipeline = Pipeline(
    "ingestion",
    "raw_extraction",
    ingestion_steps
)

ingestion_context = IngestionContext(
    logger = PipelineLogger(logging.getLogger("ingestion")),
    snapshot_path = INGESTION_SNAPSHOT,
    logs_path = INGESTION_LOGS,
    engine = engine,
    raw_schema = DB_SCHEMA,
    source_data = RAW_LIGUE1_DIR,
    col_mapping = col_mapping,
    required_cols = required_cols
)