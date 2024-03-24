from sqlalchemy import Table, select, alias
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy import exc as SQLException
import exceptions as exc
from database import SyncDatabaseInterface
from database.schemas import schedule
from typing import List

class EventDetailTableInterface(SyncDatabaseInterface):
    def __init__(
            self, 
            table_schema: Table = schedule.SCHEDULE_TABLES['event_detail'], 
            engine: AsyncEngine = schedule.async_engine,
            ignore_keys=['id']
    ) -> None:
        super().__init__(table_schema, engine, ignore_keys)