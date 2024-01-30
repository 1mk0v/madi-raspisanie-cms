from exceptions import BaseAPIException

class BaseRequestsException(BaseAPIException):
    def __init__(self, *args: object, message: str = 'Something wrong with you requests', status_code=400) -> None:
        super().__init__(*args, message=message, status_code=status_code)


class NotFoundError(BaseRequestsException):
    def __init__(self, *args: object, message: str = 'Not found url', status_code=404) -> None:
        super().__init__(*args, message=message, status_code=status_code)
