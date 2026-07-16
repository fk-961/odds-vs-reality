from abc import ABC
from dataclasses import dataclass, field
from typing import Any
from datetime import datetime
from uuid import UUID, uuid4

from .logger import PipelineLogger

@dataclass
class PipelineContext(ABC):
    # configuration
    engine : Any
    
    # runtime
    artifacts : dict[str, Any] = field(
        default_factory = dict,
        init = False
    )
    
    def get_artifact(self, table_name : str) -> Any:
        if table_name not in self.artifacts:
            raise KeyError(f"Missing artifact '{table_name}'")
        return self.artifacts[table_name]
    
@dataclass
class ExecutionContext:
    logger : PipelineLogger
    persisted_artifacts : list[str] = field(
        default_factory = list, init = False
    )
    run_id : UUID = field(
        default_factory = uuid4, init = False
    )
    timestamp : datetime = field(
        default_factory = datetime.now, init = False
    )
    
    def cascade_logger(self, logger) -> None:
        self.logger = logger
    
    def get_run_id(self) -> UUID:
        return self.run_id
    
    def get_persisted_artifacts(self) -> list[str]:
        return self.persisted_artifacts
    
    def add_successful_artifact(self, name : str) -> None:
        self.persisted_artifacts.append(name)
    