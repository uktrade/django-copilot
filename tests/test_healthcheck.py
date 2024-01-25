import pytest
import time

from dbt_copilot_python.celery_health_check import (
    healthcheck,
    liveness_probe
)
from unittest.mock import patch


@pytest.mark.usefixtures('celery_app')
def test_setup_assigns_liveliness_probe(celery_app):

    celery_app = healthcheck.setup(celery_app)

    assert celery_app.steps["worker"].pop() is\
           liveness_probe.LivenessProbe


@pytest.mark.usefixtures('celery_app')
@pytest.mark.usefixtures('celery_worker')
def test_check_health_happy_path(
    mocker,
    celery_worker,
    celery_app
):
    celery_app = healthcheck.setup(celery_app)

    time.sleep(5)
    #spy = mocker.spy(healthcheck, "on_worker_ready")
    #assert spy.call_count == 1

    with pytest.raises(SystemExit) as sys_exit_e:
        healthcheck.check_health()

    assert sys_exit_e.type == SystemExit
    assert sys_exit_e.value.code == 0
