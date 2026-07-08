from dataclasses import dataclass

from src.core.status import Status
from src.core.step import PipelineStep, StepExecutionResult
from src.core.pipeline import PipelineContext

@dataclass
class ArtifactPipeline:
    name : str
    builder : list[PipelineStep]
    validator : list[PipelineStep]
    persister : PipelineStep
    
@dataclass
class ArtifactExecutionResult:
    name : str
    status = Status
    timestamp : str
    duration_seconds : float
    result : list[StepExecutionResult]
    
class ArtifactRunner:
    
    def run(
        self,
        artifact : ArtifactPipeline,
        ctx : PipelineContext
    ) -> ArtifactExecutionResult:
        
        ctx.logger.info()