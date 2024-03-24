from sqlalchemy import (MetaData, create_engine)
from sqlalchemy.ext.asyncio import create_async_engine
from ..database import sync_schedule_url, async_schedule_url
from ..utils import get_tables


sync_engine = create_engine(sync_schedule_url, echo=False)
async_engine = create_async_engine(async_schedule_url , echo=False)
metadata = MetaData()

SCHEDULE_TABLES = get_tables(sync_engine, metadata)