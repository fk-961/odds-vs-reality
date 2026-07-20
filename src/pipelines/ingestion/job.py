from maestro import blueprints as bp

# build steps
from src.pipelines.ingestion.core.context import IngestionContext
from src.pipelines.ingestion.steps.create_schema import CreateSchema
from src.pipelines.ingestion.steps.extract_data import ExtractData
from src.pipelines.ingestion.steps.fix_columns import FixColumns
from src.pipelines.ingestion.steps.concat_tables import ConcatTables
# validate steps
from src.pipelines.validation.core.registry import get_checks
checks = get_checks("ingestion")
# persist steps
from src.db.common.persist_table import PersistTable
# context
from src.db.engine import engine
from src.config import DB_SCHEMA, RAW_LIGUE1_DIR
from src.mappings import col_mapping, required_cols

matches = bp.Artifact(
    name = "matches",
    builders = [
        CreateSchema(),
        ExtractData(),
        FixColumns(),
        ConcatTables()
    ],
    validators = checks,
    persisters = [
        PersistTable("matches", "matches")
    ],
    dependencies = []
)

ingestion_pipeline = bp.Pipeline(
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

ingestion_job = bp.PipelineExecution(
    pipeline = ingestion_pipeline,
    context = ingestion_context
)