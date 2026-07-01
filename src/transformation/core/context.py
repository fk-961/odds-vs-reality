from dataclasses import dataclass, field
from sqlalchemy.engine import Engine
from src.core.context import PipelineContext

@dataclass
class TransformationContext(PipelineContext):
    
    # configuration
    engine : Engine
    
    # runtime
    artifacts : dict[str, any] = field(default_factory = dict)
    