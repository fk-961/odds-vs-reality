from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.core.logger import PipelineLogger

@dataclass
class PipelineContext(ABC):
    logger : PipelineLogger