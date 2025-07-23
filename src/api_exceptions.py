from fastapi import HTTPException, status


# MARK: Base
class BaseBadRequestException(HTTPException):
    """Base `HTTP_400_BAD_REQUEST` exception."""

    default_message = "Bad request"

    def __init__(self):
        status_code = status.HTTP_400_BAD_REQUEST

        super().__init__(status_code=status_code, detail=self.default_message)


class BaseUnauthorizedException(HTTPException):
    """Base `HTTP_401_UNAUTHORIZED` exception."""

    default_message = "Unauthorized"

    def __init__(self):
        status_code = status.HTTP_401_UNAUTHORIZED

        super().__init__(status_code=status_code, detail=self.default_message)


class BaseForbiddenException(HTTPException):
    """Base `HTTP_403_FORBIDDEN` exception."""

    default_message = "Forbidden"

    def __init__(self):
        status_code = status.HTTP_403_FORBIDDEN

        super().__init__(status_code=status_code, detail=self.default_message)


class BaseNotFoundException(HTTPException):
    """Base `HTTP_404_NOT_FOUND` exception."""

    default_message = "Not found"

    def __init__(self):
        status_code = status.HTTP_404_NOT_FOUND

        super().__init__(status_code=status_code, detail=self.default_message)


class BaseConflictException(HTTPException):
    """Base `HTTP_409_CONFLICT` exception."""

    default_message = "Conflict"

    def __init__(self):
        status_code = status.HTTP_409_CONFLICT

        super().__init__(status_code=status_code, detail=self.default_message)
