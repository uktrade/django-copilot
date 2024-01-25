# See https://medium.com/ambient-innovation/health-checks-for-celery-in-kubernetes-cf3274a3e106

import sys
from datetime import datetime

from celery import signals
from dateutil.tz import tz

from .const import HEARTBEAT_FILE
from .const import READINESS_FILE
from .heartbeat import HeartBeat


def on_worker_ready(**_):
    print(f"READINESS_FILE: {READINESS_FILE}")
    print(f"READINESS_FILE exists before touch: {READINESS_FILE.is_file()}")
    READINESS_FILE.touch()
    print(f"READINESS_FILE exists after touch: {READINESS_FILE.is_file()}")


def setup(celery_app=None):
    signals.worker_ready.connect(on_worker_ready)

    signals.worker_shutdown.connect(lambda **_: READINESS_FILE.unlink(missing_ok=True))

    celery_app.steps["worker"].add(HeartBeat)
    return celery_app


def check_health():
    if not READINESS_FILE.is_file():
        __exit_with_message(1, "Healthcheck: Celery readiness file NOT found.")

    if not HEARTBEAT_FILE.is_file():
        __exit_with_message(1, "Healthcheck: Celery heartbeat file NOT found.")

    heartbeat_timestamp = float(HEARTBEAT_FILE.read_text())
    current_timestamp = datetime.timestamp(datetime.now(tz=tz.UTC))
    time_diff = current_timestamp - heartbeat_timestamp
    if time_diff > 60:
        __exit_with_message(1, "Healthcheck: Celery Worker heartbeat file timestamp ")

    __exit_with_message(0, "Healthcheck: Celery Worker heartbeat file found and timestamp ")


def __exit_with_message(code, message):
    print(message)
    sys.exit(code)


if __name__ == "__main__":
    check_health()
