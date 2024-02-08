from .models import UserType

USER_TYPES = [
    UserType(value='Root', priority=100),
    UserType(value='Senior admin', priority=99),
    UserType(value='Middle admin', priority=98),
    UserType(value='Junior admin', priority=97),
    UserType(value='Student', priority=96)
]