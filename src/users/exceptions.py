from exceptions import BaseAPIException

class DeleteYourselfUserError(BaseAPIException):
    def __init__(self, *args: object, detail: dict = None, message: str = "You can't delete yourself!" , status_code=400) -> None:
        super().__init__(*args, detail=detail, message=message, status_code=status_code)