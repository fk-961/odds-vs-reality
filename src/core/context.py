from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

from src.core.logger import PipelineLogger

@dataclass
class PipelineContext(ABC):
    logger : PipelineLogger
    snapshot_path : Path
    logs_path : Path