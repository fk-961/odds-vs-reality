from abc import ABC
from dataclasses import dataclass, field
from sqlalchemy.engine import Engine
from pathlib import Path
from typing import Any

from src.core.execution.logger import PipelineLogger

@dataclass
class PipelineContext(ABC):
    # configuration
    logger : PipelineLogger
    engine : Engine
    snaphot_path : Path
    
    # runtime
    artifacts : dict[str, Any] = field(
        default_factory = dict,
        init = False
    )
    
    def get_artifact(self, table_name : str) -> Any:
        if table_name not in self.artifacts:
            raise KeyError(f"Missing artifact '{table_name}'")
        return self.artifacts[table_name]