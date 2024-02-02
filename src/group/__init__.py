from sqlalchemy import Table
from database import DatabaseInterface, schemas

class GroupTableInterface(DatabaseInterface):

    def __init__(self, table_schema: Table = schemas.group, engine=schemas.schedule_engine) -> None:
        super().__init__(table_schema, engine)
    