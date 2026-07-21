from maestro import blueprints as bp

from src.pipelines.ingestion.core.context import IngestionContext
from src.pipelines.ingestion.steps.create_schema import CreateSchema
from src.pipelines.ingestion.services.build_artifacts import build_artifacts
from src.db.engine import engine
from src.config import DB_SCHEMA, RAW_LIGUE1_DIR
from src.mappings import col_mapping, required_cols

matches = bp.Artifact(
    name = "matches",
    builders = [CreateSchema()],
    validators = [],
    persisters = [],
    dependencies = []
)

file_artifacts = build_artifacts(RAW_LIGUE1_DIR)


ingestion_pipeline = bp.Pipeline(
    name = "ingestion",
    artifacts = [matches] + file_artifacts
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