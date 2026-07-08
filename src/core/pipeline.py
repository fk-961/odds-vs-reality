import logging
from abc import ABC
from dataclasses import dataclass, field
from pathlib import Path
from sqlalchemy.engine import Engine
from typing import Any

class PipelineLogger:
    
    def __init__(self, logger : logging.Logger):
        self.logger = logger
        
    def info(self, msg : str, *args):
        self.logger.info(msg, *args)
        
    def warning(self, msg : str, *args):
        self.logger.warning(msg, *args)
        
    def error(self, msg : str, *args):
        self.logger.error(msg, *args)
        
    def log_status(self, status : str, msg : str, *args):
        level_map = {
            "PASS" : self.logger.info,
            "WARNING" : self.logger.warning,
            "FAIL" : self.logger.error
        }
        level_map.get(status, self.logger.info)(msg, *args)
        
@dataclass
class PipelineContext(ABC):
    
    logger : PipelineLogger
    logs_path : Path
    snapshot_path : Path
    engine : Engine
    
    artifacts : dict[str, Any] = field(default_factory = dict)