import logging
from pathlib import Path

from maestro.common.types import Status

class PipelineLogger:
    """Defining a custom logger class that is aware of
    execution's layer (pipeline, stage, step).
    """
    
    def __init__(
        self,
        name : str,
        logs_path : Path,
        logger : logging.Logger | None = None,
        layer : dict | None = None,
    ):
        
        self.name = name
        self.logs_path = logs_path
        self.layer = layer or {}
        
        if logger:
            self._logger = logger
            return
            
        logs_path.mkdir(exist_ok = True)
        
        self._logger = logging.getLogger(name)
        self._logger.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
        )

        console = logging.StreamHandler()
        console.setFormatter(formatter)

        file = logging.FileHandler(
            logs_path/"last_run.log",
            mode="w",
            encoding="utf-8"
        )
        file.setFormatter(formatter)

        self._logger.addHandler(console)
        self._logger.addHandler(file)
        
        
    def child(self, **kwargs) -> PipelineLogger:
        """Creates a logger that is a child of the caller.
        """
        return PipelineLogger(
            name = self.name,
            logs_path = self.logs_path,
            logger = self._logger,
            layer = {
                **self.layer,
                **kwargs
            }
        )
        
    def _format(self, msg: str) -> str:
        layers = []

        if self.layer.get("orchestrator"):
            layers.append(self.layer["orchestrator"])

        if self.layer.get("pipeline"):
            layers.append(f"[{self.layer['pipeline']}]")

        if self.layer.get("artifact"):
            layers.append(self.layer["artifact"])

        if self.layer.get("stage"):
            layers.append(f"[{self.layer['stage']}]")

        if not layers:
            return msg

        return " | ".join(layers) + " | " + msg
    
    def info(self, msg : str, *args, **kwargs):
        self._logger.info(
            self._format(msg), *args, **kwargs
        )
        
    def warning(self, msg : str, *args, **kwargs):
        self._logger.warning(
            self._format(msg), *args, **kwargs
        )
        
    def error(self, msg : str, *args, **kwargs):
        self._logger.error(
            self._format(msg), *args, **kwargs
        )
        
    def log_status(self, status : Status, msg : str, *args, **kwargs):
        level_map = {
            Status.PASS : self.info,
            Status.WARNING : self.warning,
            Status.FAIL : self.error
        }
        
        level_map.get(status, self.info)(msg, *args, **kwargs)
        