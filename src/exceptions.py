class BaseAPIException(BaseException):

    def __init__(self, *args: object, message:str = 'Base API exception!', status_code) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(*args)

class ClientException(BaseAPIException):

    def __init__(self, *args: object, message: str = 'Somethink wrong with you request', status_code = 400) -> None:
        super().__init__(*args, message=message, status_code=status_code)