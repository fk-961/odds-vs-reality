from enum import Enum

class Status(str, Enum):
    PASS = "PASS"
    WARNING = "WARNING"
    FAIL = "FAIL"
    
class Stage(str, Enum):
    BUILD = "BUILD"
    VALIDATE = "VALIDATE"
    PERSIST = "PERSIST"
    
    @property
    def abort_on_fail(self):
        return self != Stage.VALIDATE