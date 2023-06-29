import os
from unittest.mock import patch

import requests
import requests_mock

from dbt_copilot_python.network import get_container_ip


def test_get_container_ip_not_in_copilot_returns_none():
    assert "ECS_CONTAINER_METADATA_URI_V4" not in os.environ

    assert not get_container_ip()


@patch.dict(
    os.environ, {"ECS_CONTAINER_METADATA_URI_V4": "http://test.com"}, clear=True
)
def test_get_container_ip_request_exception_returns_none():
    with requests_mock.Mocker() as mock:
        mock.get("http://test.com", exc=requests.exceptions.RequestException)

        assert not get_container_ip()


@patch.dict(
    os.environ, {"ECS_CONTAINER_METADATA_URI_V4": "http://test.com"}, clear=True
)
def test_get_container_ip_success():
    mock_response = {"Networks": [{"IPv4Addresses": ["1.1.1.1"]}]}

    with requests_mock.Mocker() as mock:
        mock.get("http://test.com", json=mock_response)

        assert get_container_ip() == "1.1.1.1"
