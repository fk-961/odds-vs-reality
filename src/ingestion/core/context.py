from dataclasses import dataclass, field
from sqlalchemy.engine import Engine
from pathlib import Path

from src.core.context import PipelineContext


# mutable pipeline context
@dataclass
class IngestionContext(PipelineContext):
    
    # configuration
    engine : Engine
    raw_schema : Path
    source_data : Path
    col_mapping : dict[str, str]
    
    # runtime
    artifacts : dict[str, any] = field(default_factory = dict)