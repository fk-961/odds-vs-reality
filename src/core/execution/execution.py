from dataclasses import dataclass, field
from uuid import uuid4, UUID
from datetime import datetime

from src.core.execution.logger import PipelineLogger

@dataclass
class Execution:
    run_id : UUID = field(
        default_factory = uuid4, init = False
    )
    
    timestamp : datetime = field(
        default_factory = datetime.now, init = False
    )