from sqlalchemy import Engine, Table
from database import SyncDatabaseInterface
from database.schemas import schedule

class GroupTableInterface(SyncDatabaseInterface):
    def __init__(
            self,
            table_schema: Table = schedule.SCHEDULE_TABLES['group'], 
            engine: Engine=schedule.sync_engine,
            ignore_keys=["id"]
    ) -> None:
        super().__init__(table_schema, engine, ignore_keys)

class TeacherTableInterface(SyncDatabaseInterface):
    def __init__(
            self,
            table_schema: Table = schedule.SCHEDULE_TABLES['group'], 
            engine: Engine=schedule.sync_engine,
            ignore_keys=["id"]
    ) -> None:
        super().__init__(table_schema, engine, ignore_keys)