"""
Validation Checks are used on created tables.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict
from sqlalchemy.engine import Engine

class ValidationCheck(ABC):
    
    name : str
        
    @abstractmethod
    def run(self, engine : Engine) -> CheckResult:
        pass
    

@dataclass
class CheckResult:
    status : str
    result : Dict[str, Any]
    
@dataclass
class CheckExecutionResult:
    name : str
    status : str
    duration_seconds : float
    timestamp : str
    result : Dict[str, Any]