import logging
logging.basicConfig(
    level = logging.INFO,
    format = "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
)

from src.core.orchestrator import PipelineMaestro
from src.core.runner import PipelineRunner
from src.core.report_builder import ReportBuilder

from src.ingestion.pipeline import (
    ingestion_pipeline, ingestion_context
)
from src.validation.pipeline import (
    validation_pipeline, validation_context
)
from src.transformation.pipeline import (
    transformation_pipeline, transformation_context
)

if __name__ == "__main__":
    pipeline_runs = [
        (ingestion_pipeline, ingestion_context),
        (validation_pipeline, validation_context),
        (transformation_pipeline, transformation_context)
    ]
    
    executor = PipelineMaestro(
        pipeline_runs = pipeline_runs,
        runner = PipelineRunner(),
        report_builder = ReportBuilder()
    )
    
    executor.execute()