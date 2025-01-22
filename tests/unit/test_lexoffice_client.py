import pytest
import responses
from lexoffice_py.client import Lexoffice
from lexoffice_py.errors import (
    BadRequestError, UnauthorizedError, PaymentRequiredError, ForbiddenError, NotFoundError,
    MethodNotAllowedError, NotAcceptableError, ConflictError, UnsupportedMediaTypeError,
    TooManyRequestsError, ServerError, NotImplementedError, ServiceUnavailableError, GatewayTimeoutError,
    LexofficeAPIError
)

import time
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
        (429, TooManyRequestsError),  # Note: Handled in client logic as per the comment in the function
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
    with pytest.raises(TooManyRequestsError):
        client._request(path="test_path")