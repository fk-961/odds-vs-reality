import logging

class PipelineLogger:
    def __init__(self, logger : logging.Logger):
        self.logger = logger
        
    def info(self, msg, *args):
        self.logger.info(msg, *args)
        
    def warning(self, msg, *args):
        self.logger.warning(msg, *args)
        
    def error(self, msg, *args):
        self.logger.error(msg, *args)
        
    def log_status(self, status : str, message : str, *args):
        level_map = {
            "PASS" : self.logger.info,
            "WARNING" : self.logger.warning,
            "FAIL" : self.logger.error
        }
        level_map.get(status, self.logger.info)(message, *args)