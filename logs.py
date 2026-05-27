import time


def follow_log(log_file):
    with open(log_file, "r") as f:
        f.seek(0, 2)

        while True:
            line = f.readline()

            if not line:
                time.sleep(0.2)
                continue

            yield line