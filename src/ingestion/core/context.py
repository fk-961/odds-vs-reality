from dataclasses import dataclass, field
from sqlalchemy.engine import Engine
from pathlib import Path
from src.core.logger import PipelineLogger

# mutable pipeline context
@dataclass
class IngestionContext:
    
    # configuration
    engine : Engine
    logger : PipelineLogger
    raw_schema : Path
    source_data : Path
    col_mapping : dict[str, str]
    
    # runtime
    artifacts : dict[str, any] = field(default_factory = dict)