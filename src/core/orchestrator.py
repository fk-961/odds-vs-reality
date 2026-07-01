from typing import Tuple

from src.core.pipeline import Pipeline
from src.core.runner import PipelineRunner
from src.core.context import PipelineContext
from src.core.report_builder import ReportBuilder

class PipelineMaestro:
    
    def __init__(
        self,
        pipeline_runs : list[Tuple[Pipeline, PipelineContext]],
        runner : PipelineRunner,
        report_builder : ReportBuilder
    ):
        self.pipeline_runs = pipeline_runs
        self.runner = runner
        self. report_builder = report_builder
        
    def execute(self) -> None:
        for pipeline, context in self.pipeline_runs:
            run_result = self.runner.run(
                pipeline, context
            )
            
            self.report_builder.add_snapshot(run_result, context.snapshot_path)
            self.report_builder.add_logs(run_result, context.logs_path)