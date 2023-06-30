import os
from unittest.mock import patch

import pytest
import requests
import requests_mock

from dbt_copilot_python.network import setup_allowed_hosts


@pytest.fixture
def allowed_hosts() -> list[str]:
    return ["0.0.0.0"]


def test_setup_allowed_hosts_with_not_copilot_does_not_add_ip(allowed_hosts: list[str]):
    assert "ECS_CONTAINER_METADATA_URI_V4" not in os.environ

    allowed_hosts = setup_allowed_hosts(allowed_hosts)

    assert allowed_hosts == ['0.0.0.0']


@patch.dict(
    os.environ, {"ECS_CONTAINER_METADATA_URI_V4": "http://test.com"}, clear=True
)
def test_setup_allowed_hosts_with_exception_does_not_add_ip(allowed_hosts):
    with requests_mock.Mocker() as mock:
        mock.get("http://test.com", exc=requests.exceptions.RequestException)

        allowed_hosts = setup_allowed_hosts(allowed_hosts)

        assert allowed_hosts == ['0.0.0.0']


@patch.dict(
    os.environ, {"ECS_CONTAINER_METADATA_URI_V4": "http://test.com"}, clear=True
)
def test_setup_allowed_hosts_with_copilot_adds_ip(allowed_hosts):
    mock_response = {"Networks": [{"IPv4Addresses": ["1.1.1.1"]}]}

    with requests_mock.Mocker() as mock:
        mock.get("http://test.com", json=mock_response)

        allowed_hosts = setup_allowed_hosts(allowed_hosts)

        assert allowed_hosts == ['0.0.0.0', '1.1.1.1']
