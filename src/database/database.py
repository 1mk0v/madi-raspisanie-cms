from .utils import get_db_url
from .config import *

SYNC_DRIVER = 'psycopg'
ASYNC_DRIVER = 'asyncpg'

sync_schedule_url = get_db_url(
    db_driver=SYNC_DRIVER,
    user=DB_SCHEDULE_USER,
    password=DB_SCHEDULE_PASSWORD,
    host=DB_SCHEDULE_HOST,
    name=DB_SCHEDULE_NAME
)

sync_cms_url = get_db_url(
    db_driver=SYNC_DRIVER,
    user=DB_CMS_USER,
    password=DB_CMS_PASSWORD,
    host=DB_CMS_HOST,
    name=DB_CMS_NAME
)

async_schedule_url = get_db_url(
    db_driver=ASYNC_DRIVER,
    user=DB_SCHEDULE_USER,
    password=DB_SCHEDULE_PASSWORD,
    host=DB_SCHEDULE_HOST,
    name=DB_SCHEDULE_NAME
)

async_cms_url = get_db_url(
    db_driver=ASYNC_DRIVER,
    user=DB_CMS_USER,
    password=DB_CMS_PASSWORD,
    host=DB_CMS_HOST,
    name=DB_CMS_NAME
)