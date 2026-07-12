from src.core.execution.context import ExecutionContext
from src.core.execution.logger import PipelineLogger
from src.core.framework.orchestrator import (
    Maestro, MaestroRunner
)
from src.core.execution.writer import ExecutionWriter
from src.ingestion.pipeline import ingestion_job

def main():
    
    # Define current run session
    # Generates session specific info like run id and timestamp
    session = ExecutionContext(
        logger = PipelineLogger()
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
    
    writer = ExecutionWriter()
    writer.run(result)
    
if __name__ == "__main__":
    main()