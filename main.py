import json
import os

import requests


def is_copilot():
    """Are we running in copilot/ECS?"""
    return "ECS_CONTAINER_METADATA_URI_V4" in os.environ


def get_container_ip():
    """Get the private IP of the container;

    Usage in settings.py:

    private_ip = get_container_ip()

    if private_ip:
        ALLOWED_HOSTS.append(private_ip)

    """

    if is_copilot():
        try:
            aws_metadata = requests.get(
                os.environ["ECS_CONTAINER_METADATA_URI_V4"], timeout=0.01
            ).json()
            return aws_metadata["Networks"][0]["IPv4Addresses"][0]
        except requests.exceptions.RequestException:
            pass


def setup_database(environment_key, **extra_keys):
    """Take a Copilot database environment variable and return the django configuration"""
    config = json.loads(os.environ[environment_key])

    return {
        "ENGINE": f"django.db.backends.{config['engine']}",
        "NAME": config["dbname"],
        "USER": config["username"],
        "PASSWORD": config["password"],
        "HOST": config["host"],
        "PORT": config["port"],
        **extra_keys,
    }


def database_from_env(environment_key, **extra_keys):
    """Set up the default django database from a Copilot database environment variable

    Usage in settings.py:

    DATABASES = database_from_env("MY_DATABASE")
    """

    return {"default": setup_database(environment_key, **extra_keys)}
