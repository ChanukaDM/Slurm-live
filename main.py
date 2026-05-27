import sys
import threading
import time

from slurm import get_job_info
from logs import follow_log
from ui import render_header, print_log


REFRESH_SECONDS = 5


class JobWatcher:
    def __init__(self, job_id):
        self.job_id = job_id
        self.running = True

    def monitor_status(self):
        while self.running:
            info = get_job_info(self.job_id)

            if info:
                state = info.get("job_state", "UNKNOWN")
                if state in ["COMPLETED", "FAILED", "CANCELLED", "TIMEOUT"]:
                    print(f"\nJob finished with state: {state}")
                    self.running = False
                    break

            time.sleep(REFRESH_SECONDS)

    def start(self):
        info = get_job_info(self.job_id)

        if not info:
            print("Could not find job.")
            return

        log_file = info["stdout"]

        print(f"Watching: {log_file}\n")

        render_header(self.job_id, info)

        monitor_thread = threading.Thread(target=self.monitor_status)
        monitor_thread.start()
        try:
            for line in follow_log(log_file):
                if not self.running:
                    break

                print_log(line)

        except KeyboardInterrupt:
            print("\nStopped monitoring.")
            self.running = False


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <job_id>")
        sys.exit(1)

    job_id = sys.argv[1]

    watcher = JobWatcher(job_id)
    watcher.start()