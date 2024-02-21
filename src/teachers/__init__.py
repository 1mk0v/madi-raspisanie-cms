from sqlalchemy import Engine, Table
from database import DatabaseInterface, schemas

class TeacherTableInterface(DatabaseInterface):
    def __init__(self, table_schema: Table = schemas.teacher, engine: Engine=schemas.schedule_engine,
                 ignore_keys=['id']) -> None:
        super().__init__(table_schema, engine, ignore_keys)