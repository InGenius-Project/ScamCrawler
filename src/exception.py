class RequestException(Exception):
    def __init__(self, message: str, status_code: int):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__} [{self.status_code}]: {self.message}"
    
class NotFoundException(RequestException):
    def __init__(self, message="URL not found."):
        status_code = 404
        super().__init__(message, status_code)

class AccessDeniedException(RequestException):
    def __init__(self, message="Access Denied."):
        status_code = 403
        super().__init__(message, status_code)

class UnauthorizedException(RequestException):
    def __init__(self, message="Unauthorized."):
        status_code = 401
        super().__init__(message, status_code)