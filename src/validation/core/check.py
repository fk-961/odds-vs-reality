"""
Validation Checks are used on created tables.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from src.validation.core.context import ValidationContext

class ValidationCheck(ABC):
    
    name : str
        
    @abstractmethod
    def run(self, ctx : ValidationContext) -> CheckResult:
        pass
    

@dataclass
class CheckResult:
    status : str
    result : dict[str, any]
    
@dataclass
class CheckExecutionResult:
    name : str
    status : str
    duration_seconds : float
    timestamp : str
    result : dict[str, any]