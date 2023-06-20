import json
import os
import pytest

import requests
import requests_mock
from unittest.mock import patch

from main import database_from_env, get_container_ip, is_copilot, setup_database


TEST_CONN = {
    "dbClusterIdentifier": "cluster-identifier",
    "username": "postgres",
    "password": "test-password",
    "dbname": "main",
    "engine": "postgres",
    "port": 5432,
    "host": "hostname.com",
}


@pytest.mark.parametrize(
    "environ,output",
    [
        ({"ECS_CONTAINER_METADATA_URI_V4": "https://fake/url"}, True),
        ({}, False),
    ],
)
def test_is_copilot(environ, output):
    with patch.dict(os.environ, environ, clear=True):
        assert is_copilot() == output


def test_setup_database():
    with patch.dict(os.environ, {"DATABASE_CONFIG": json.dumps(TEST_CONN)}, clear=True):
        assert setup_database("DATABASE_CONFIG") == {
            "ENGINE": f"django.db.backends.{TEST_CONN['engine']}",
            "NAME": TEST_CONN["dbname"],
            "USER": TEST_CONN["username"],
            "PASSWORD": TEST_CONN["password"],
            "HOST": TEST_CONN["host"],
            "PORT": TEST_CONN["port"],
        }


def test_database_from_env():
    with patch.dict(os.environ, {"DATABASE_CONFIG": json.dumps(TEST_CONN)}, clear=True):
        assert database_from_env("DATABASE_CONFIG") == {
            "default": setup_database("DATABASE_CONFIG")
        }


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
