import logging
from src.core.logger import PipelineLogger
logging.basicConfig(
    level = logging.INFO,
    format = "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
)

from src.core.pipeline import Pipeline
from src.core.runner import PipelineRunner

# Ingestion Steps
from src.ingestion.steps.create_schema import CreateSchema
from src.ingestion.steps.extract_data import ExtractData
from src.ingestion.steps.fix_columns import FixColumns
from src.ingestion.steps.load_data import LoadData

# Validation Checks
from src.validation.core.registry import load_all_checks, get_checks

# Transformation Steps
from src.transformation.steps.load_matches import LoadMatches
from src.transformation.steps.build_standings import BuildStandings
from src.transformation.steps.build_teams import BuildTeams
from src.transformation.steps.build_match_probs import BuildMatchProbs
from src.transformation.steps.build_expected_points import BuildExpectedPoints
from src.transformation.steps.build_expected_standings import BuildExpectedStandings
from src.transformation.steps.persist_table import PersistTable

# Run and contexts
from src.ingestion.core.context import IngestionContext
from src.validation.core.context import ValidationContext
from src.transformation.core.context import TransformationContext
from src.db.engine import engine
from src.config import DB_SCHEMA, RAW_LIGUE1_DIR
from src.mappings import col_mapping

# Reporting
from src.core.report_builder import ReportBuilder
from src.config import (
    INGESTION_SNAPSHOT, INGESTION_LOGS,
    VALIDATION_SNAPSHOT, VALIDATION_LOGS,
    TRANSFORMATION_SNAPSHOT, TRANSFORMATION_LOGS
)


if __name__ == "__main__":
    
    ### Ingestion Pipeline
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
    
    ### Validation Pipeline
    load_all_checks()
    checks = get_checks()
    
    validation_pipeline = Pipeline(
        "validation",
        "data_quality",
        steps = checks
    )
    
    ### Transformation Pipeline
    transformation_steps = [
        LoadMatches(),
        BuildStandings(),
        PersistTable("standings", "standings"),
        BuildTeams(),
        PersistTable("teams", "teams"),
        BuildMatchProbs(),
        PersistTable("match_probs", "match_probs"),
        BuildExpectedPoints(),
        PersistTable("expected_points", "expected_points"),
        BuildExpectedStandings(),
        PersistTable("expected_standings", "expected_standings")
    ]
    
    transformation_pipeline = Pipeline(
        "transformation",
        "data_transformation",
        steps = transformation_steps
    )
    
    ### Runner
    runner = PipelineRunner()
    logger = PipelineLogger(logging.getLogger("pipeline"))
    
    # ingestion
    ingestion_context = IngestionContext(
        logger = logger,
        engine = engine,
        raw_schema = DB_SCHEMA,
        source_data = RAW_LIGUE1_DIR,
        col_mapping = col_mapping
    )
    
    ingestion_result = runner.run(
        ingestion_pipeline, ingestion_context
    )
    
    # validation
    validation_context = ValidationContext(
        logger = logger,
        engine = engine
    )
    
    validation_result = runner.run(
        validation_pipeline, validation_context
    )
    
    # transformation context
    transformation_context = TransformationContext(
        logger = logger,
        engine = engine
    )
    
    transformation_result = runner.run(
        transformation_pipeline, transformation_context
    )
    
    ### Logs
    report_builder = ReportBuilder()
    
    # ingestion
    report_builder.add_snapshot(ingestion_result, INGESTION_SNAPSHOT)
    report_builder.add_logs(ingestion_result, INGESTION_LOGS)
    
    # validation
    report_builder.add_snapshot(validation_result, VALIDATION_SNAPSHOT)
    report_builder.add_logs(validation_result, VALIDATION_LOGS)
    
    # transformation
    report_builder.add_snapshot(transformation_result, TRANSFORMATION_SNAPSHOT)
    report_builder.add_logs(transformation_result, TRANSFORMATION_LOGS)