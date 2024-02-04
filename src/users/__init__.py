from sqlalchemy import Table
from database import DatabaseInterface, schemas

class UserTableInterface(DatabaseInterface):

    def __init__(self, table_schema: Table = schemas.user, engine=schemas.cms_engine) -> None:
        super().__init__(table_schema, engine)
    