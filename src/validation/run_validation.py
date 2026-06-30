import logging

from src.config import (
    VALIDATION_LOGS,
    VALIDATION_SNAPSHOT,
    ROOT_DIR
)

from src.db.engine import engine
from src.validation.core.registry import load_all_checks, get_checks

from src.validation.core.pipeline import ValidationPipeline
from src.validation.core.runner import ValidationRunner
from src.validation.core.context import ValidationContext
from src.core.logger import PipelineLogger
from src.validation.core.report_builder import ValidationReportBuilder

logging.basicConfig(
    level = logging.INFO,
    format = "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
)

if __name__ == "__main__":
    load_all_checks()
    
    ingestion_validation = ValidationPipeline(
        name = "ingestion",
        checks = get_checks()
    )
    
    runner = ValidationRunner()
    
    results = runner.run(
        ingestion_validation,
        ValidationContext(engine, PipelineLogger(logging.getLogger("validation")))
    )
    
    report_builder = ValidationReportBuilder(
        VALIDATION_SNAPSHOT, VALIDATION_LOGS
    )
    
    report_builder.add_snapshot(results)
    report_builder.add_logs(results)