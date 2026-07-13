from src.core.framework.orchestrator import Maestro
from src.core.execution.executor import MaestroExecutor
from src.ingestion.job import ingestion_job
from src.transformation.job import transformation_job
from src.analytics.job import analytics_job

def main():
    
    jobs = Maestro(
        jobs = [
            ingestion_job,
            transformation_job,
            analytics_job
        ]
    )
    
    executor = MaestroExecutor()
    executor.execute(jobs)
    
    
if __name__ == "__main__":
    main()