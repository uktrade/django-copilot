from datetime import datetime

from celery import bootsteps
from dateutil.tz import tz

from .const import HEARTBEAT_FILE


# Todo: Should we call this "HeartBeat"?
class LivenessProbe(bootsteps.StartStopStep):
    requires = {"celery.worker.components:Timer"}

    def __init__(self, parent, **kwargs):
        print("LivenessProbe.__init__")
        super().__init__(parent, **kwargs)
        self.requests = []
        self.tref = None

    def start(self, worker):
        print("LivenessProbe.start")
        self.tref = worker.timer.call_repeatedly(
            1.0,
            self.update_heartbeat_file,
            (worker,),
            priority=10,
        )

    def stop(self, worker):
        print("LivenessProbe.stop")
        HEARTBEAT_FILE.unlink(missing_ok=True)

    def update_heartbeat_file(self, worker):
        print("LivenessProbe.update_heartbeat_file")
        print(f"HEARTBEAT_FILE: {HEARTBEAT_FILE}")
        HEARTBEAT_FILE.write_text(str(datetime.timestamp(datetime.now(tz=tz.UTC))))
        print(f"HEARTBEAT_FILE contents after update: {HEARTBEAT_FILE.read_text()}")
