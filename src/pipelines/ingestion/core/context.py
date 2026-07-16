from dataclasses import dataclass
from pathlib import Path

from maestro import runtime as rt

@dataclass
class IngestionContext(rt.PipelineContext):
    
    raw_schema : Path
    source_data : Path
    col_mapping : dict[str, str]
    required_cols : set