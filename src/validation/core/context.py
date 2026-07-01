from dataclasses import dataclass
from sqlalchemy.engine import Engine
from src.core.context import PipelineContext

@dataclass
class ValidationContext(PipelineContext):
    engine : Engine