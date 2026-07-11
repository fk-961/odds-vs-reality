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
    
def get_overall_status(results : list) -> Status:
    statuses = [r.status for r in results]
    
    if Status.FAIL in statuses:
        return Status.FAIL
    if Status.WARNING in statuses:
        return Status.WARNING
    return Status.PASS