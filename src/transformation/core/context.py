from dataclasses import dataclass, field
from sqlalchemy.engine import Engine
from src.core.logger import PipelineLogger

@dataclass
class TransformationContext:
    
    # configuration
    logger : PipelineLogger
    engine : Engine
    
    # runtime
    artifacts : dict[str, any] = field(default_factory = dict)
    