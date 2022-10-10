class ApiResponseError(Exception):
    """Exception raised when the API returns an error response."""

class NotAuthenticatedError(Exception):
    """Exception raised when the error code return 102."""

class BannedIPError(Exception):
    """Exception raised when the account was banned."""