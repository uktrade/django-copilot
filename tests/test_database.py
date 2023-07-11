import json
import os
from unittest.mock import patch

from dbt_copilot_python.database import database_from_env
from dbt_copilot_python.database import database_url_from_env
from dbt_copilot_python.database import setup_database

TEST_CONN = {
    "dbClusterIdentifier": "cluster-identifier",
    "username": "postgres",
    "password": "test-password",
    "dbname": "main",
    "engine": "postgres",
    "port": 5432,
    "host": "hostname.com",
}


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


def test_setup_database_extra_keys():
    extra_keys = {"extra1": "test", "extra2": "test2"}

    with patch.dict(os.environ, {"DATABASE_CONFIG": json.dumps(TEST_CONN)}, clear=True):
        assert setup_database("DATABASE_CONFIG", **extra_keys) == {
            "ENGINE": f"django.db.backends.{TEST_CONN['engine']}",
            "NAME": TEST_CONN["dbname"],
            "USER": TEST_CONN["username"],
            "PASSWORD": TEST_CONN["password"],
            "HOST": TEST_CONN["host"],
            "PORT": TEST_CONN["port"],
            **extra_keys,
        }


def test_database_from_env():
    with patch.dict(os.environ, {"DATABASE_CONFIG": json.dumps(TEST_CONN)}, clear=True):
        assert database_from_env("DATABASE_CONFIG") == {
            "default": setup_database("DATABASE_CONFIG")
        }


def test_database_url_from_env():
    with patch.dict(os.environ, {"DATABASE_CONFIG": json.dumps(TEST_CONN)}, clear=True):
        assert (
            database_url_from_env("DATABASE_CONFIG")
            == "postgres://postgres:test-password@hostname.com:5432/main"
        )
