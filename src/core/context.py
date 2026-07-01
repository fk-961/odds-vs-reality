from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from sqlalchemy.engine import Engine

from src.core.logger import PipelineLogger

@dataclass
class PipelineContext(ABC):
    
    # configuration
    logger : PipelineLogger
    snapshot_path : Path
    logs_path : Path
    engine : Engine
    
    # runtime
    artifacts : dict[str, any] = field(
        default_factory = dict,
        init = False
    )