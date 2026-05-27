import subprocess
import re


def run_command(command):
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True
    )

    return result.stdout.strip()


def get_job_info(job_id):
    command = f"scontrol show job {job_id}"
    output = run_command(command)
    
    if not output:
        return None

    info = {}

    patterns = {
        "job_state": r"JobState=(\w+)",
        "run_time": r"RunTime=([^ ]+)",
        "stdout": r"StdOut=(\S+)",
        "node_list": r"NodeList=(\S+)"
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, output)

        if match:
            info[key] = match.group(1)
        else:
            info[key] = "Unknown"

    return info