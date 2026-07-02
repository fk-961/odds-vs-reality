from dataclasses import dataclass, field
from pathlib import Path

from src.core.context import PipelineContext

@dataclass
class IngestionContext(PipelineContext):
    
    raw_schema : Path
    source_data : Path
    col_mapping : dict[str, str]
    required_cols : set