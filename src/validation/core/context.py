from dataclasses import dataclass
from sqlalchemy.engine import Engine
from src.core.context import PipelineContext
from src.core.logger import PipelineLogger

@dataclass
class ValidationContext(PipelineContext):
    logger : PipelineLogger
    engine : Engine