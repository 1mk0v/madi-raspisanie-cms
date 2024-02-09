from starlette.status import HTTP_400_BAD_REQUEST
from exceptions import BaseAPIException 
from fastapi import status

class AuthException(BaseAPIException):
    def __init__(self, *args: object, message: str = "Authentication error!", status_code = status.HTTP_400_BAD_REQUEST) -> None:
        super().__init__(*args, message = message, status_code = status_code)


class NotFoundUserError(AuthException):
    def __init__(self, *args: object, status_code = status.HTTP_404_NOT_FOUND,
                  message:str = "User don't found!") -> None:
        super().__init__(*args, message = message, status_code = status_code)

class IncorrectPasswordError(AuthException):
    def __init__(self, *args: object, status_code = status.HTTP_400_BAD_REQUEST,
                 message: str = "Incorrect password!",) -> None:
        super().__init__(*args, message = message, status_code = status_code)

class UserAlreadyRegistredError(AuthException):
    def __init__(self, *args: object, message: str = "This user already registred!", status_code=status.HTTP_400_BAD_REQUEST) -> None:
        super().__init__(*args, message=message, status_code=status_code)

class RegistHigherRankingUserError(BaseAPIException):
    def __init__(self, *args: object, detail: dict = None, message: str = "You cannot regist a user higher than you in rank!" , status_code=400) -> None:
        super().__init__(*args, detail=detail, message=message, status_code=status_code)