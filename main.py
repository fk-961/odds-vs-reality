import logging
logging.basicConfig(
    level = logging.INFO,
    format = "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
)

from src.core.execution.context import ExecutionContext
from src.core.execution.logger import PipelineLogger
from src.core.framework.orchestrator import (
    Maestro, MaestroRunner
)
from src.ingestion.pipeline import ingestion_job

def main():
    
    # Define current run session
    # Generates session specific info like run id and timestamp
    session = ExecutionContext(
        logger = PipelineLogger(
            logging.getLogger(__name__)
        )
    )
    
    # Define maestro runner that executes the pipelines
    runner = MaestroRunner()
    
    # Define jobs
    jobs = Maestro(
        jobs = [
            ingestion_job
        ]
    )
    
    # execute
    result = runner.execute(jobs, session)
    
if __name__ == "__main__":
    main()