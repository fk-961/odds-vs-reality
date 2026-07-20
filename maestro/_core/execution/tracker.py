from datetime import datetime
from time import perf_counter


class ExecutionTracker:
    def __enter__(self):
        self.timestamp = datetime.now().isoformat()
        self.start = perf_counter()
        self.end = None
        return self

    def __exit__(self, *_):
        self.end = perf_counter()

    @property
    def duration(self):
        end = self.end or perf_counter()
        return round(end - self.start, 5)