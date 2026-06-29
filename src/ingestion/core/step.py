"""
IngestionStep class that defines every step of our ingestion
pipeline like column renaming and null values handling.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass

class IngestionStep(ABC):
    name : str
    
    def run(self) -> StepResult:
        pass

    
@dataclass
class StepResult:
    name : str
    result : dict[str, any]
