from sqlalchemy import (
    Table, Column, 
    Integer, String, MetaData, 
    ForeignKey, DateTime, create_engine
)
from sqlalchemy.ext.asyncio import create_async_engine
from ..database import sync_cms_url, async_cms_url

sync_engine = create_engine(sync_cms_url, echo=True)
async_engine = create_async_engine(async_cms_url, echo=True)
metadata = MetaData()

user = Table(
    'user',
    metadata,
    Column('id', Integer, primary_key=True, unique=True),
    Column('login', String),
    Column('hashed_password', String)
)
user_type = Table(
    'user_type',
    metadata,
    Column('value', String),
    Column('priority', Integer, primary_key=True, unique=True)
)
user_info = Table(
    'user_info',
    metadata,
    Column('user_id', Integer, ForeignKey("user.id")),
    Column('name', String),
    Column('priority', Integer, ForeignKey("user_type.priority"))
)
cms_settings = Table(
    'settings',
    metadata,
    Column('id', Integer, primary_key=True, unique=True),
    Column('name', String),
    Column('value', Integer)
)
history = Table(
    'history',
    metadata,
    Column('host', String, nullable=True),
    Column('user_id', Integer, ForeignKey("user.id"), nullable=True),
    Column('action', String),
    Column('date', DateTime),
    Column('detail', String)
)
metadata.create_all(sync_engine)