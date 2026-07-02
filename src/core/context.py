from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from sqlalchemy.engine import Engine
from typing import Any

from src.core.logger import PipelineLogger

@dataclass
class PipelineContext(ABC):
    
    # configuration
    logger : PipelineLogger
    snapshot_path : Path
    logs_path : Path
    engine : Engine
    
    # runtime
    artifacts : dict[str, Any] = field(
        default_factory = dict,
        init = False
    )
    
    def get_artifact(self, key : str) -> Any:
        if key not in self.artifacts:
            raise KeyError(f"Missing artifact '{key}'")
        return self.artifacts[key]