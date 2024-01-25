from datetime import datetime
from datetime import timedelta

import pytest
from dateutil.tz import tz

from dbt_copilot_python.celery_health_check import healthcheck
from dbt_copilot_python.celery_health_check.const import HEARTBEAT_FILE
from dbt_copilot_python.celery_health_check.const import READINESS_FILE
from dbt_copilot_python.celery_health_check.heartbeat import HeartBeat


def clean_up():
    print("Clean up")
    READINESS_FILE.unlink(missing_ok=True)
    assert READINESS_FILE.is_file() is False
    HEARTBEAT_FILE.unlink(missing_ok=True)
    assert HEARTBEAT_FILE.is_file() is False


@pytest.fixture
def setup_and_teardown():
    clean_up()
    yield
    clean_up()


@pytest.mark.usefixtures("celery_app")
def test_setup_assigns_liveliness_probe(setup_and_teardown, celery_app):
    celery_app = healthcheck.setup(celery_app)

    assert celery_app.steps["worker"].pop() is HeartBeat


def test_check_health_happy_path(setup_and_teardown):
    fake_celery_setup(ready=True, alive="alive")

    with pytest.raises(SystemExit) as sys_exit_e:
        healthcheck.check_health()

    assert sys_exit_e.type == SystemExit
    assert sys_exit_e.value.code == 0


def test_check_health_not_ready(setup_and_teardown):
    fake_celery_setup(ready=False, alive="not_started")

    with pytest.raises(SystemExit) as sys_exit_e:
        healthcheck.check_health()

    assert sys_exit_e.type == SystemExit
    assert sys_exit_e.value.code == 1


def test_check_health_not_alive_liveness_probe_not_started(setup_and_teardown):
    fake_celery_setup(ready=True, alive="not_started")

    with pytest.raises(SystemExit) as sys_exit_e:
        healthcheck.check_health()

    assert sys_exit_e.type == SystemExit
    assert sys_exit_e.value.code == 1


def test_check_health_not_alive_has_died(setup_and_teardown):
    fake_celery_setup(ready=True, alive="died")

    with pytest.raises(SystemExit) as sys_exit_e:
        healthcheck.check_health()

    assert sys_exit_e.type == SystemExit
    assert sys_exit_e.value.code == 1


def fake_celery_setup(ready, alive):
    """We could not get Celery signals working in the context of the unit tests,
    so are faking the interactions it would have with the file system here."""
    if ready:
        healthcheck.on_worker_ready()

    if alive == "alive":
        HEARTBEAT_FILE.write_text(str(datetime.timestamp(datetime.now(tz=tz.UTC))))
    elif alive == "died":
        HEARTBEAT_FILE.write_text(
            str(datetime.timestamp(datetime.now(tz=tz.UTC) - timedelta(minutes=1)))
        )
