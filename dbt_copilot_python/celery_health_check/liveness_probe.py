import tempfile
from datetime import datetime
from pathlib import Path

from celery import bootsteps
from dateutil.tz import tz

from .healthcheck import HEARTBEAT_FILE


class LivenessProbe(bootsteps.StartStopStep):
    requires = {"celery.worker.components:Timer"}

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.requests = []
        self.tref = None

    def start(self, worker):
        self.tref = worker.timer.call_repeatedly(
            1.0,
            self.update_heartbeat_file,
            (worker,),
            priority=10,
        )

    def stop(self, worker):
        HEARTBEAT_FILE.unlink(missing_ok=True)

    def update_heartbeat_file(self, worker):
        HEARTBEAT_FILE.write_text(str(datetime.timestamp(datetime.now(tz=tz.UTC))))
