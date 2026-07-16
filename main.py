from maestro import blueprints as bp
from maestro import runtime as rt
from maestro import execution as ex

from src.pipelines.ingestion.job import ingestion_job
from src.pipelines.transformation.job import transformation_job
from src.pipelines.analytics.job import analytics_job
from src.reporting.writer import ExecutionWriter
from src.db.engine import engine
from src.config import LOGS_DIR

def main():
    
    jobs = bp.Maestro(
        jobs = [
            ingestion_job,
            transformation_job,
            analytics_job
        ]
    )
    
    executor = ex.MaestroExecutor(
        logger = rt.PipelineLogger(
            name = "analytics_pipeline",
            logs_path = LOGS_DIR
        )
    )
    results = executor.execute(jobs)
    
    writer = ExecutionWriter()
    writer.run(
        exec_result = results,
        metadata_engine = engine,
        logs_path = LOGS_DIR
    )
    
    
if __name__ == "__main__":
    main()