import os
from unittest.mock import patch

import pytest

from dbt_copilot_python.utility import is_copilot


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
