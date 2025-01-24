import pytest
from lexoffice_py.client import Lexoffice
from lexoffice_py.errors import ClientNotAuthorizedError

def test_initialization_with_client_secret():
    client_secret = "test_secret"
    client = Lexoffice(client_secret=client_secret, max_retries=5, default_retry_wait=2)

    assert client.client_secret == client_secret
    assert client.headers["Authorization"] == f"Bearer {client_secret}"
    assert client.headers["Accept"] == "application/json"
    assert client.max_retries == 5
    assert client.default_retry_wait == 2
    assert client.BASE_URL == "https://api.lexoffice.io"


import os
from unittest.mock import patch

@patch.dict(os.environ, {"CLIENT_SECRET": "env_secret"})
def test_initialization_with_env_variable():
    client = Lexoffice(client_secret=None)

    assert client.client_secret == "env_secret"
    assert client.headers["Authorization"] == "Bearer env_secret"
    assert client.headers["Accept"] == "application/json"

@patch.dict(os.environ, {"CLIENT_SECRET": ""})
def test_initialization_without_client_secret():
    with pytest.raises(ClientNotAuthorizedError) as exc_info:
        client = Lexoffice(client_secret=None)