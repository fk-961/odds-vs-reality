from datetime import datetime
from time import perf_counter

class ExecutionTracker:
    def __enter__(self):
        self.timestamp = datetime.now().isoformat()
        self.start = perf_counter()
        return self

    def __exit__(self, *_):
        self.duration = round(
            perf_counter() - self.start,
            5
        )