import responses
import pytest
from lexoffice_py.client import Lexoffice
from lexoffice_py.errors import NotFoundError

@responses.activate
def test_get_some_data():
    # Mock the API response
    responses.add(
        responses.GET,
        "https://api.lexoffice.io/test_path",
        json={"data": "mocked response"},
        status=200,
    )

    # Initialize the client
    client = Lexoffice(client_secret='test_key')

    # Call the method
    response = client._request(path='test_path')

    # Assertions
    assert response == {"data": "mocked response"}

@responses.activate
def test_get_some_data_404_not_found():
    responses.add(
        responses.GET,
        "https://api.lexoffice.io/test_path",
        status=404,
    )
    client = Lexoffice(client_secret='test_key')

    with pytest.raises(NotFoundError):
        client._request(path='test_path')