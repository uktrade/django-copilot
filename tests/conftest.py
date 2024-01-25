import pytest


@pytest.fixture(scope="session")
def celery_config():
    return {"result_backend": "redis://"}


@pytest.fixture(scope="session")
def celery_worker_parameters():
    return {"without_heartbeat": False}
