from dataclasses import dataclass
from sqlalchemy.engine import Engine
from src.core.logger import PipelineLogger

@dataclass
class ValidationContext:
    engine : Engine
    logger : PipelineLogger