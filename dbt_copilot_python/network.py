import os

import requests

from dbt_copilot_python.utility import is_copilot


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
