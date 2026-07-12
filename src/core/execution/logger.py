import logging

from src.core.framework.types import Status

class PipelineLogger:
    """Defining a custom logger class that is aware of
    execution's layer (pipeline, stage, step).
    """
    
    def __init__(
        self,
        logger : logging.Logger,
        layer : dict | None = None
    ):
        self.logger = logger
        self.layer = layer or {}
        
    def child(self, **kwargs) -> PipelineLogger:
        """Creates a logger that is a child of the caller.
        """
        return PipelineLogger(
            logger = self.logger,
            layer = {
                **self.layer,
                **kwargs
            }
        )
        
    def _format(self, msg : str) -> str:
        
        layers = []
        if "orchestrator" in self.layer:
            layers.append(self.layer['orchestrator'])
        if "pipeline" in self.layer:
            layers.append(f"[{self.layer['pipeline']}]")
        if "artifact" in self.layer:
            layers.append(self.layer['artifact'])
        if "stage" in self.layer:
            layers.append(f"[{self.layer['stage']}]")
        
        prefix = " | ".join(layers)
        return prefix + " | " + msg
    
    def info(self, msg : str, *args, **kwargs):
        self.logger.info(
            self._format(msg), *args, **kwargs
        )
        
    def warning(self, msg : str, *args, **kwargs):
        self.logger.warning(
            self._format(msg), *args, **kwargs
        )
        
    def error(self, msg : str, *args, **kwargs):
        self.logger.error(
            self._format(msg), *args, **kwargs
        )
        
    def log_status(self, status : Status, msg : str, *args, **kwargs):
        level_map = {
            Status.PASS : self.info,
            Status.WARNING : self.warning,
            Status.FAIL : self.error
        }
        
        level_map.get(status, self.info)(msg, *args, **kwargs)
        