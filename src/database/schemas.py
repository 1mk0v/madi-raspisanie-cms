from sqlalchemy import (
    Table, Column, Sequence, 
    Integer, String, MetaData, 
    ForeignKey, DateTime, create_engine
)

from .config import (
    DB_SCHEDULE_HOST, DB_SCHEDULE_NAME, DB_SCHEDULE_PASSWORD, DB_SCHEDULE_USER,
    DB_CMS_HOST, DB_CMS_NAME, DB_CMS_PASSWORD, DB_CMS_USER
)

def get_db_url(user, password, host, name):
    return f"postgresql+psycopg://{user}:{password}@{host}/{name}"

schedule_engine = create_engine(
    get_db_url(DB_SCHEDULE_USER, DB_SCHEDULE_PASSWORD, DB_SCHEDULE_HOST, DB_SCHEDULE_NAME),
    echo=False
)
schedule_metadata = MetaData()

#--------MADI Schedule API Database PSQL--------#

auditorium_id_seq = Sequence('auditorium_id_seq', schedule_metadata)   
date_id_seq = Sequence('date_id_seq', schedule_metadata)         
department_id_seq = Sequence('department_id_seq', schedule_metadata)   
discipline_id_seq = Sequence('discipline_id_seq', schedule_metadata)   
exam_info_id_seq = Sequence('exam_info_id_seq', schedule_metadata)    
frequency_id_seq = Sequence('frequency_id_seq', schedule_metadata)    
group_id_seq = Sequence('group_id_seq', schedule_metadata)        
schedule_info_id_seq = Sequence('schedule_info_id_seq', schedule_metadata)
teacher_id_seq = Sequence('teacher_id_seq', schedule_metadata)      
time_id_seq = Sequence('time_id_seq', schedule_metadata)         
type_id_seq = Sequence('type_id_seq', schedule_metadata)         
weekday_id_seq = Sequence('weekday_id_seq', schedule_metadata)


auditorium = Table(
    'auditorium',
    schedule_metadata, 
    Column("id", Integer, auditorium_id_seq, server_default=auditorium_id_seq.next_value() , primary_key=True),
    autoload_with=schedule_engine,
    extend_existing=True
)          
date = Table(
    'date', 
    schedule_metadata,
    Column("id", Integer, date_id_seq, server_default=date_id_seq.next_value() , primary_key=True), 
    autoload_with=schedule_engine,
    extend_existing=True
)                
department = Table(
    'department',
    schedule_metadata,
    Column("id", Integer, department_id_seq, server_default=department_id_seq.next_value() , primary_key=True), 
    autoload_with=schedule_engine,
    extend_existing=True
)
discipline = Table(
    'discipline',
    schedule_metadata,
    Column("id", Integer, discipline_id_seq, server_default=discipline_id_seq.next_value() , primary_key=True), 
    autoload_with=schedule_engine,
    extend_existing=True
)          
exam_info = Table(
    'exam_info', 
    schedule_metadata,
    Column("id", Integer, exam_info_id_seq, server_default=exam_info_id_seq.next_value() , primary_key=True), 
    autoload_with=schedule_engine,
    extend_existing=True
)           
frequency = Table(
    'frequency', 
    schedule_metadata,
    Column("id", Integer, frequency_id_seq, server_default=frequency_id_seq.next_value() , primary_key=True),
    autoload_with=schedule_engine,
    extend_existing=True
)           
group = Table(
    'group', 
    schedule_metadata,
    Column("id", Integer, group_id_seq, server_default=group_id_seq.next_value() , primary_key=True),
    autoload_with=schedule_engine,
    extend_existing=True
)               
schedule_info = Table(
    'schedule_info', 
    schedule_metadata,
    Column("id", Integer, schedule_info_id_seq, server_default=schedule_info_id_seq.next_value() , primary_key=True),
    autoload_with=schedule_engine,
    extend_existing=True
)       
teacher = Table(
    'teacher', 
    schedule_metadata,
    Column("id", Integer, teacher_id_seq, server_default=teacher_id_seq.next_value() , primary_key=True), 
    autoload_with=schedule_engine,
    extend_existing=True
)             
time = Table(
    'time', 
    schedule_metadata, 
    Column("id", Integer, time_id_seq, server_default=time_id_seq.next_value() , primary_key=True),
    autoload_with=schedule_engine,
    extend_existing=True
)                
type = Table(
    'type', 
    schedule_metadata,
    Column("id", Integer, type_id_seq, server_default=type_id_seq.next_value() , primary_key=True),
    autoload_with=schedule_engine,
    extend_existing=True
)                
weekday = Table(
    'weekday', 
    schedule_metadata,
    Column("id", Integer, weekday_id_seq, server_default=weekday_id_seq.next_value() , primary_key=True),
    autoload_with=schedule_engine,
    extend_existing=True
)



#--------MADI CMS API Database PSQL--------#

cms_metadata = MetaData()

user = Table(
    'user',
    cms_metadata,
    Column('id', Integer, primary_key=True, unique=True),
    Column('login', String),
    Column('hashed_password', String)
)
user_info = Table(
    'user_info',
    cms_metadata,
    Column('user_id', Integer, ForeignKey("user.id")),
    Column('name', String),
    Column('type_id', Integer, ForeignKey("user_type.id"))
)
user_type = Table(
    'user_type',
    cms_metadata,
    Column('id', Integer),
    Column('value', String),
    Column('priority', Integer)
)
cms_settings = Table(
    'settings',
    cms_metadata,
    Column('id', Integer),
    Column('name', String),
    Column('value', Integer)
)
history = Table(
    'history',
    cms_metadata,
    Column('host', String, nullable=True),
    Column('user_id', Integer, ForeignKey("user.id"), nullable=True),
    Column('action', String),
    Column('date', DateTime),
    Column('detail', String)
)

cms_engine = create_engine(
    get_db_url(DB_CMS_USER, DB_CMS_PASSWORD, DB_CMS_HOST, DB_CMS_NAME), 
    echo=False
)
cms_metadata.create_all(cms_engine)