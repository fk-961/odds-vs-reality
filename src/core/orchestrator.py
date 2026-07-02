from typing import Tuple

from datetime import datetime
from time import perf_counter

from src.core.pipeline import Pipeline
from src.core.runner import PipelineRunner
from src.core.context import PipelineContext
from src.core.logger import PipelineLogger
from src.core.report_builder import ReportBuilder

class PipelineMaestro:
    
    def __init__(
        self,
        pipeline_runs : list[Tuple[Pipeline, PipelineContext]],
        runner : PipelineRunner,
        logger : PipelineLogger,
        report_builder : ReportBuilder
    ):
        self.pipeline_runs = pipeline_runs
        self.runner = runner
        self.logger = logger
        self. report_builder = report_builder
        
    def execute(self) -> None:
        divider = "="*100
        timestamp = datetime.now().isoformat()
        start = perf_counter()
        
        self.logger.info(
            """Starting Pipeline Execution
Pipelines scheduled: %s
%s""",
            len(self.pipeline_runs),
            divider
        
        )
        
        for pipeline, ctx in self.pipeline_runs:
            self.logger.info(
                "Running %s pipeline\n%s",
                pipeline.name,
                divider
            )
            run_result = self.runner.run(
                pipeline, ctx
            )
            
            self.report_builder.add_snapshot(run_result, ctx.snapshot_path)
            self.report_builder.add_logs(run_result, ctx.logs_path)
            
            if run_result.status == "FAIL" and pipeline.stop_on_fail:
                ctx.logger.error(
                    "ABORT Execution: [%s] failed", pipeline.name
                )
                break
            
        self.logger.info(
            "\n%s\nExecution Summary: Duration %ss",
            divider,
            round(perf_counter() - start, 5)
        )