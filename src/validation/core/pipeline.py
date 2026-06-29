from dataclasses import dataclass

from src.validation.core.check import (
    ValidationCheck, CheckResult, CheckExecutionResult
)

class ValidationPipeline:
    
    def __init__(
        self,
        name : str,
        checks : list[ValidationCheck]
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
    result : list[CheckExecutionResult]