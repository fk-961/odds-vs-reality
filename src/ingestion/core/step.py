"""
IngestionStep class that defines every step of our ingestion
pipeline like column renaming and null values handling.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from src.ingestion.core.context import IngestionContext

class IngestionStep(ABC):
    name : str
    
    def run(self, ctx : IngestionContext) -> StepResult:
        pass

    
@dataclass
class StepResult:
    status : str
    result : dict[str, any]
    
@dataclass
class StepExecutionResult:
    name : str
    status : str
    duration_seconds : float
    timestamp : str
    result : dict[str, any]
