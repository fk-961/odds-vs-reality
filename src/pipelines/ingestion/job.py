from src.ingestion.core.context import IngestionContext
from maestro import Artifact

from src.core.framework.pipeline import Pipeline
from src.core.framework.orchestrator import PipelineExecution

from src.ingestion.steps.create_schema import CreateSchema
from src.ingestion.steps.extract_data import ExtractData
from src.ingestion.steps.fix_columns import FixColumns
from src.ingestion.steps.concat_tables import ConcatTables
from src.core.common_steps.persist_table import PersistTable

from src.db.engine import engine
from src.config import DB_SCHEMA, RAW_LIGUE1_DIR
from src.mappings import col_mapping, required_cols

matches = Artifact(
    name = "matches",
    builders = [
        CreateSchema(),
        ExtractData(),
        FixColumns(),
        ConcatTables()
    ],
    validators = [],
    persisters = [
        PersistTable("matches", "matches")
    ],
    dependencies = []
)

ingestion_pipeline = Pipeline(
    name = "ingestion",
    artifacts = [matches]
)

ingestion_context = IngestionContext(
    engine = engine,
    raw_schema = DB_SCHEMA,
    source_data = RAW_LIGUE1_DIR,
    col_mapping = col_mapping,
    required_cols = required_cols
)

ingestion_job = PipelineExecution(
    pipeline = ingestion_pipeline,
    context = ingestion_context
)