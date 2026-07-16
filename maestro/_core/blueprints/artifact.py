"""
Instances of Artifact represent the combination of the necessary
steps required to create a specific table. It is defined by 3
stages: build, validate and persist each composed of steps.
"""
from dataclasses import dataclass, field
from uuid import UUID
from datetime import datetime

from .step import PipelineStep, StepExecutionResult
from maestro.common.types import Status, Stage

@dataclass
class Artifact:
    name : str
    builders : list[PipelineStep]
    validators : list[PipelineStep]
    persisters : list[PipelineStep]
    dependencies : list[str]
    stages : list[Stage] = field(
        default_factory = lambda: [
            Stage.BUILD, Stage.VALIDATE, Stage.PERSIST
        ],
        init = False
    )
    
    def get_builders(self) -> list[PipelineStep]:
        return self.builders
    
    def get_validators(self) -> list[PipelineStep]:
        return self.validators
    
    def get_persisters(self) -> list[PipelineStep]:
        return self.persisters
    
    def get_dependencies(self) -> list[str]:
        return self.dependencies
    
    def get_stages(self) -> list[Stage]:
        return self.stages
    

@dataclass
class StageExecutionResult:
    run_id : UUID
    stage : Stage
    artifact_name : str
    scheduled_steps : int
    timestamp : datetime
    duration_seconds : float
    status : Status
    steps_attempted : int
    steps_warnings_count : int
    stage_results : list[StepExecutionResult] | None = None
    message : str | None = None
    error : str | None = None
    
@dataclass
class ArtifactExecutionResult:
    run_id : UUID
    name : str
    timestamp : datetime
    duration_seconds : float
    status : Status
    artifact_results : list[StageExecutionResult] | None = None
    message : str | None = None
    error : str | None = None
