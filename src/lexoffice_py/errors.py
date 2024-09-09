class LexofficeAPIError(Exception):
    """Base class for all lexoffice API exceptions."""
    def __init__(self, message="An error occurred with the lexoffice API"):
        self.message = message
        super().__init__(self.message)

class BadRequestError(LexofficeAPIError):
    def __init__(self):
        super().__init__("400 Bad Request: Malformed syntax or a bad query.")

class UnauthorizedError(LexofficeAPIError):
    def __init__(self):
        super().__init__("401 Unauthorized: Action requires user authentication.")

class PaymentRequiredError(LexofficeAPIError):
    def __init__(self):
        super().__init__("402 Payment Required: Action not accessible due to a lexoffice contract issue.")

class ForbiddenError(LexofficeAPIError):
    def __init__(self):
        super().__init__("403 Forbidden: Authenticated but insufficient scope or insufficient access rights.")

class NotFoundError(LexofficeAPIError):
    def __init__(self):
        super().__init__("404 Not Found: Requested resource does not exist (anymore).")

class MethodNotAllowedError(LexofficeAPIError):
    def __init__(self):
        super().__init__("405 Method Not Allowed: Method not allowed on resource.")

class NotAcceptableError(LexofficeAPIError):
    def __init__(self):
        super().__init__("406 Not Acceptable: Validation issues due to invalid data.")

class ConflictError(LexofficeAPIError):
    def __init__(self):
        super().__init__("409 Conflict: Request not allowed due to the current state of the resource.")

class UnsupportedMediaTypeError(LexofficeAPIError):
    def __init__(self):
        super().__init__("415 Unsupported Media Type: Missing Content-Type header or incorrect Content-Type.")

class TooManyRequestsError(LexofficeAPIError):
    def __init__(self):
        super().__init__("429 Too Many Requests: Rate limit exceeded. Retry later.")

class ServerError(LexofficeAPIError):
    def __init__(self):
        super().__init__("500 Server Error: Internal server error. Contact support.")

class NotImplementedError(LexofficeAPIError):
    def __init__(self):
        super().__init__("501 Not Implemented: Requested HTTP operation not supported.")

class ServiceUnavailableError(LexofficeAPIError):
    def __init__(self):
        super().__init__("503 Service Unavailable: Unable to handle the request temporarily.")

class GatewayTimeoutError(LexofficeAPIError):
    def __init__(self):
        super().__init__("504 Gateway Timeout: The request timed out. The request might have been processed.")

def handle_response(response):
    status_code = response.status_code
    if status_code == 200:
        return response.json()
    elif status_code == 201:
        return response.json()
    elif status_code == 202:
        return response.json()
    elif status_code == 204:
        return
    elif status_code == 400:
        raise BadRequestError()
    elif status_code == 401:
        raise UnauthorizedError()
    elif status_code == 402:
        raise PaymentRequiredError()
    elif status_code == 403:
        raise ForbiddenError()
    elif status_code == 404:
        raise NotFoundError()
    elif status_code == 405:
        raise MethodNotAllowedError()
    elif status_code == 406:
        raise NotAcceptableError()
    elif status_code == 409:
        raise ConflictError()
    elif status_code == 415:
        raise UnsupportedMediaTypeError()
    # this is handled in the client
    # elif status_code == 429:
    #     raise TooManyRequestsError()
    elif status_code == 500:
        raise ServerError()
    elif status_code == 501:
        raise NotImplementedError()
    elif status_code == 503:
        raise ServiceUnavailableError()
    elif status_code == 504:
        raise GatewayTimeoutError()
    else:
        raise LexofficeAPIError("Unexpected error occurred.")