import json
import time

class PipelineStats:

    def __init__(self):
        self.start = time.time()
        self.files_processed = 0

    def file_done(self):
        self.files_processed += 1

    def save(self, path):

        runtime = time.time() - self.start

        stats = {
            "files_processed": self.files_processed,
            "runtime_seconds": runtime
        }

        with open(path, "w") as f:
            json.dump(stats, f, indent=4)