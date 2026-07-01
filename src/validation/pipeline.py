import logging
from src.core.logger import PipelineLogger
from src.core.pipeline import Pipeline

from src.validation.core.context import ValidationContext
from src.validation.core.registry import load_all_checks, get_checks

from src.config import VALIDATION_SNAPSHOT, VALIDATION_LOGS
from src.db.engine import engine

load_all_checks()
checks = get_checks()

validation_pipeline = Pipeline(
    "validation",
    "data_quality",
    steps = checks
)

validation_context = ValidationContext(
    logger = PipelineLogger(logging.getLogger("validation")),
    snapshot_path = VALIDATION_SNAPSHOT,
    logs_path = VALIDATION_LOGS,
    engine = engine
)