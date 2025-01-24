import pytest
import responses
from lexoffice_py.client import Lexoffice
from lexoffice_py.errors import (
    BadRequestError, UnauthorizedError, PaymentRequiredError, ForbiddenError, NotFoundError,
    MethodNotAllowedError, NotAcceptableError, ConflictError, UnsupportedMediaTypeError,
    TooManyRequestsError, ServerError, NotImplementedError, ServiceUnavailableError, GatewayTimeoutError,
    LexofficeAPIError, MaxRetriesError
)
from unittest.mock import patch, MagicMock
from unittest.mock import patch

# Fixture for the Lexoffice client
@pytest.fixture
def client():
    return Lexoffice(client_secret='test_key')

# Helper function to add mocked responses
def add_mock_response(method, url, status, json=None):
    responses.add(method, url, json=json, status=status)

# Parameterized tests for all error responses
@pytest.mark.parametrize(
    "status,expected_exception",
    [
        (400, BadRequestError),
        (401, UnauthorizedError),
        (402, PaymentRequiredError),
        (403, ForbiddenError),
        (404, NotFoundError),
        (405, MethodNotAllowedError),
        (406, NotAcceptableError),
        (409, ConflictError),
        (415, UnsupportedMediaTypeError),
        (429, MaxRetriesError),  # Note: Handled in client logic as per the comment in the function
        (500, ServerError),
        (501, NotImplementedError),
        (503, ServiceUnavailableError),
        (504, GatewayTimeoutError),
    ],
)
@responses.activate
def test_handle_response_errors(client, status, expected_exception):
    add_mock_response(
        method=responses.GET,
        url="https://api.lexoffice.io/test_path",
        status=status,
    )

    with pytest.raises(expected_exception):
        client._request(path='test_path')

# Test for unexpected errors
@responses.activate
def test_handle_unexpected_error(client):
    add_mock_response(
        method=responses.GET,
        url="https://api.lexoffice.io/test_path",
        status=418,  # Example of an unhandled status code
    )

    with pytest.raises(LexofficeAPIError) as exc_info:
        client._request(path='test_path')


@responses.activate
@patch("time.sleep", return_value=None)  # Mock sleep to speed up the test
def test_handle_response_429_too_many_requests(mock_sleep, client):
    # Mock the 429 response for all retries
    for _ in range(client.max_retries):
        responses.add(
            responses.GET,
            "https://api.lexoffice.io/test_path",
            status=429,
        )

    # Test that the client retries and eventually raises TooManyRequestsError
    with pytest.raises(MaxRetriesError):
        client._request(path="test_path")

@responses.activate
def test_request_success():
    # Mock API response
    add_mock_response(
        method=responses.GET,
        url="https://api.lexoffice.io/test-path",
        status=200,
        json={"success": True, "data": "test_data"},
    )

    # Initialize Lexoffice client
    client = Lexoffice(client_secret="test_secret")

    # Call the private `_request` method
    response = client._request(method="GET", path="/test-path")

    # Assertions
    assert response == {"success": True, "data": "test_data"}
    assert len(responses.calls) == 1
    assert responses.calls[0].request.headers["Authorization"] == "Bearer test_secret"
    assert responses.calls[0].request.url == "https://api.lexoffice.io/test-path"

@responses.activate
def test_request_unauthorized():
    # Mock a 401 Unauthorized response
    add_mock_response(
        method=responses.GET,
        url="https://api.lexoffice.io/test-path",
        status=401,
        json={"error": "Unauthorized"},
    )

    # Initialize Lexoffice client
    client = Lexoffice(client_secret="test_secret")

    # Call the private `_request` method and expect an exception
    with pytest.raises(UnauthorizedError) as exc_info:
        client._request(method="GET", path="/test-path")
    
    # Assertions
    assert "Unauthorized" in str(exc_info.value)
    assert len(responses.calls) == 1
    assert responses.calls[0].response.status_code == 401

@responses.activate
def test_request_server_error():
    # Mock a 500 Internal Server Error response
    add_mock_response(
        method=responses.GET,
        url="https://api.lexoffice.io/test-path",
        status=500,
        json={"error": "Internal server error"},
    )

    # Initialize Lexoffice client
    client = Lexoffice(client_secret="test_secret")

    # Call the private `_request` method and expect a custom exception
    with pytest.raises(ServerError) as exc_info:
        client._request(method="GET", path="/test-path")
    
    # Assertions
    assert "Internal server error" in str(exc_info.value)
    assert len(responses.calls) == 1
    assert responses.calls[0].response.status_code == 500

@responses.activate
def test_request_timeout():
    # Mock a timeout exception
    responses.add(
        method=responses.GET,
        url="https://api.lexoffice.io/test-path",
        status=504,
    )

    client = Lexoffice(client_secret="test_secret")

    # Call the private `_request` method and expect a timeout exception
    with pytest.raises(GatewayTimeoutError) as exc_info:
        client._request(method="GET", path="/test-path")
    
    assert len(responses.calls) == 1