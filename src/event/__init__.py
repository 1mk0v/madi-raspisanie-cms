from sqlalchemy import Table, select, alias
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy import exc as SQLException
import exceptions as exc
from database import SyncDatabaseInterface
from database.schemas import schedule
from .models import LessonInfo
from typing import List

class EventTableInterface(SyncDatabaseInterface):
    def __init__(
            self, 
            table_schema: Table = schedule.SCHEDULE_TABLES['event'], 
            engine: AsyncEngine = schedule.async_engine,
            ignore_keys=['id']
    ) -> None:
        super().__init__(table_schema, engine, ignore_keys)

    def _get_all_events_subquery():
        e = alias(schedule.SCHEDULE_TABLES['event'])
        ed = alias(schedule.SCHEDULE_TABLES['event_detail'])
        group = schedule.SCHEDULE_TABLES['group']
        teacher = schedule.SCHEDULE_TABLES['teacher']
        time = schedule.SCHEDULE_TABLES['time']
        return (
            select(
                e.c['date'],
                select(ed.c['value']).where(ed.c['id'] == e.c['frequency_id']).label('frequency'),
                select(ed.c['value']).where(ed.c['id'] == e.c['weekday_id']).label('weekday'),
                select(ed.c['value']).where(ed.c['id'] == e.c['discipline_id']).label('discipline'),
                select(ed.c['value']).where(ed.c['id'] == e.c['type_id']).label('type'),
                select(ed.c['value']).where(ed.c['id'] == e.c['auditorium_id']).label('auditorium'),
                select(
                    group.c['id'].label('group_id'),
                    group.c['department_id'].label('group_department_id'),
                    group.c['year'].label('group_year'),
                    group.c['value'].label('group_value')
                ).where(e.c['group_id'] == group.c['id']).subquery('group'),
                select(
                    teacher.c['id'].label('teacher_id'),
                    teacher.c['department_id'].label('teacher_department_id'),
                    teacher.c['year'].label('teacher_year'),
                    teacher.c['value'].label('teacher_value')
                ).where(e.c['teacher_id'] == teacher.c['id']).subquery(),
                select(time.c['start'], time.c['end'],).where(ed.c['id'] == e.c['event_time_id']).subquery()
            ).subquery('lesson_info')
        )

    async def get_lessons(self, limit:int = 10, offset:int = 0):
        try:
            subquery = self._get_all_events_subquery()
            query = select(subquery).where(subquery.c['type'] != 'exam')\
                .limit(limit).offset(offset)
            async with self.engine.connect() as conn:
                return await conn.execute(query)
        except SQLException.SQLAlchemyError as error:
            raise exc.BaseAPIException(message=error.args, status_code=500)
        
    async def get(self, event_type:str, limit:int = 10, offset:int = 0):
        try:
            subquery = self._get_all_events_subquery()
            query = select(subquery).where(subquery.c['type'] == event_type)\
                .limit(limit).offset(offset)
            async with self.engine.connect() as conn:
                return await conn.execute(query)
        except SQLException.SQLAlchemyError as error:
            raise exc.BaseAPIException(message=error.args, status_code=500)

    async def add(self, data:LessonInfo):
        try:
            print(data.model_dump())
        except SQLException.SQLAlchemyError as error:
            raise exc.BaseAPIException(message=error.args, status_code=500)