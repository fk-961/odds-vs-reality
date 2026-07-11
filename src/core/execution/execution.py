from dataclasses import dataclass, field
from uuid import uuid4, UUID
from datetime import datetime

from src.core.execution.logger import PipelineLogger

@dataclass
class Execution:
    logger : PipelineLogger
    persisted_artifacts : list[str]
    run_id : UUID = field(
        default_factory = uuid4, init = False
    )
    timestamp : datetime = field(
        default_factory = datetime.now, init = False
    )
    
    def get_run_id(self) -> UUID:
        return self.run_id
    
    def get_persisted_artifacts(self) -> list[str]:
        return self.persisted_artifacts
    
    def add_successful_artifact(self, name : str) -> None:
        self.persisted_artifacts.append(name)