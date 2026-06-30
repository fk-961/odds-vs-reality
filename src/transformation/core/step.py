from dataclasses import dataclass
from abc import ABC, abstractmethod

from src.transformation.core.context import TransformationContext

class TransformationStep(ABC):
    name : str
    
    @abstractmethod
    def run(self, ctx : TransformationContext) -> None:
        pass
    