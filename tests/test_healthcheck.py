import time

import pytest

from dbt_copilot_python.celery_health_check import healthcheck
from dbt_copilot_python.celery_health_check import liveness_probe
from dbt_copilot_python.celery_health_check.const import HEARTBEAT_FILE
from dbt_copilot_python.celery_health_check.const import READINESS_FILE


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

    assert celery_app.steps["worker"].pop() is liveness_probe.LivenessProbe


@pytest.mark.usefixtures("celery_app")
@pytest.mark.usefixtures("celery_worker")
def test_check_health_happy_path(setup_and_teardown, mocker, celery_worker, celery_app):
    celery_app = healthcheck.setup(celery_app)

    time.sleep(5)
    # spy = mocker.spy(healthcheck, "on_worker_ready")
    # assert spy.call_count == 1

    # healthcheck.on_worker_ready()

    with pytest.raises(SystemExit) as sys_exit_e:
        healthcheck.check_health()

    assert sys_exit_e.type == SystemExit
    assert sys_exit_e.value.code == 0
