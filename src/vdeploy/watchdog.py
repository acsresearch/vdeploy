import os
import subprocess
import multiprocessing
import time
import json
from datetime import datetime
from contextlib import contextmanager
from pathlib import Path

DEFAULT_PATH = "/root/watchdog"
DEFAULT_TIMEOUT = 60  # minutes


def start_watchdog(path, timeout):
    print("Starting watchdog at", path, "with timeout", timeout)
    with open(path, "w") as f:
        f.write(json.dumps({"pid": os.getpid(), "timeout": timeout}))

    sleep_time = timeout * 60 / 10.0
    while True:
        time.sleep(sleep_time)
        mtime = datetime.fromtimestamp(os.path.getmtime(path))
        diff = datetime.now() - mtime
        if diff.total_seconds() > timeout:
            break

    print("Timeout reached")
    subprocess.check_call(["vastai", "destroy", "instance", os.environ["CONTAINER_ID"]])


def _watchdog_task(path, timeout):
    sleep_time = timeout * 60 / 5.0
    path = Path(path)
    while True:
        path.touch()
        time.sleep(sleep_time)


@contextmanager
def keep_alive(path=DEFAULT_PATH):
    with open(path, "r") as f:
        config = json.loads(f.read())
    timeout = config["timeout"]
    watchdog_proc = multiprocessing.Process(target=_watchdog_task, args=(timeout,))
    watchdog_proc.start()
    yield
    watchdog_proc.terminate()
