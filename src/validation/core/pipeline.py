from dataclasses import dataclass
from typing import List
from sqlalchemy.engine import Engine

from src.validation.core.check import (
    ValidationCheck, CheckResult, CheckExecutionResult
)

class ValidationPipeline:
    
    def __init__(
        self,
        name : str,
        checks : List[ValidationCheck]
    ):
        self.name = name
        self.checks = checks
    
    
@dataclass
class ValidationExecutionResult:
    name : str
    status : str
    warnings : int
    fails : int
    duration_seconds : float
    timestamp : str
    result : List[CheckExecutionResult]