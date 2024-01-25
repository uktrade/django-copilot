import pytest  


@pytest.fixture(scope="session")
def celery_config():
    return {
        'result_backend': 'redis://'
    }
