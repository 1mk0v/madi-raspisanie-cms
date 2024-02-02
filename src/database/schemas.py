from sqlalchemy import Table, Column, Sequence, Integer, MetaData, create_engine
from .config import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER

DB_URL = f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"


engine = create_engine(DB_URL, echo=False)
metadata = MetaData()

auditorium_id_seq = Sequence('auditorium_id_seq', metadata)   
date_id_seq = Sequence('date_id_seq', metadata)         
department_id_seq = Sequence('department_id_seq', metadata)   
discipline_id_seq = Sequence('discipline_id_seq', metadata)   
exam_info_id_seq = Sequence('exam_info_id_seq', metadata)    
frequency_id_seq = Sequence('frequency_id_seq', metadata)    
group_id_seq = Sequence('group_id_seq', metadata)        
schedule_info_id_seq = Sequence('schedule_info_id_seq', metadata)
teacher_id_seq = Sequence('teacher_id_seq', metadata)      
time_id_seq = Sequence('time_id_seq', metadata)         
type_id_seq = Sequence('type_id_seq', metadata)         
weekday_id_seq = Sequence('weekday_id_seq', metadata)


auditorium = Table(
    'auditorium',
    metadata, 
    Column("id", Integer, auditorium_id_seq, server_default=auditorium_id_seq.next_value() , primary_key=True),
    autoload_with=engine
)          
date = Table(
    'date', 
    metadata,
    Column("id", Integer, date_id_seq, server_default=date_id_seq.next_value() , primary_key=True), 
    autoload_with=engine
)                
department = Table(
    'department',
    metadata,
    Column("id", Integer, department_id_seq, server_default=department_id_seq.next_value() , primary_key=True), 
    autoload_with=engine
)          
discipline = Table(
    'discipline',
    metadata,
    Column("id", Integer, discipline_id_seq, server_default=discipline_id_seq.next_value() , primary_key=True), 
    autoload_with=engine
)          
exam_info = Table(
    'exam_info', 
    metadata,
    Column("id", Integer, exam_info_id_seq, server_default=exam_info_id_seq.next_value() , primary_key=True), 
    autoload_with=engine
)           
frequency = Table(
    'frequency', 
    metadata,
    Column("id", Integer, frequency_id_seq, server_default=frequency_id_seq.next_value() , primary_key=True),
    autoload_with=engine
)           
group = Table(
    'group', 
    metadata,
    Column("id", Integer, group_id_seq, server_default=group_id_seq.next_value() , primary_key=True),
    autoload_with=engine
)               
schedule_info = Table(
    'schedule_info', 
    metadata,
    Column("id", Integer, schedule_info_id_seq, server_default=schedule_info_id_seq.next_value() , primary_key=True),
    autoload_with=engine
)       
teacher = Table(
    'teacher', 
    metadata,
    Column("id", Integer, teacher_id_seq, server_default=teacher_id_seq.next_value() , primary_key=True), 
    autoload_with=engine
)             
time = Table(
    'time', 
    metadata, 
    Column("id", Integer, time_id_seq, server_default=time_id_seq.next_value() , primary_key=True),
    autoload_with=engine
)                
type = Table(
    'type', 
    metadata,
    Column("id", Integer, type_id_seq, server_default=type_id_seq.next_value() , primary_key=True),
    autoload_with=engine
)                
weekday = Table(
    'weekday', 
    metadata,
    Column("id", Integer, weekday_id_seq, server_default=weekday_id_seq.next_value() , primary_key=True),
    autoload_with=engine
)