from typing import List
from pydantic import BaseModel
from sqlalchemy import Engine, Table
import sqlalchemy.exc as SQLException
import exceptions as exc
from database import DatabaseInterface, schemas
from date import DateTableInterface

class ScheduleTableInterface(DatabaseInterface):
    def __init__(self, table_schema: Table = schemas.schedule_info, engine: Engine=schemas.schedule_engine) -> None:
        self.auditorium = DatabaseInterface(schemas.auditorium, schemas.schedule_engine, ['id', 'department_id'])
        self.date = DateTableInterface()
        self.department = DatabaseInterface(schemas.department, schemas.schedule_engine)
        self.discipline = DatabaseInterface(schemas.discipline, schemas.schedule_engine, ['id'])
        self.exam_info = DatabaseInterface(schemas.exam_info, schemas.schedule_engine)
        self.frequency = DatabaseInterface(schemas.frequency, schemas.schedule_engine, ['id'])
        self.group = DatabaseInterface(schemas.group, schemas.schedule_engine, ['year'])
        self.teacher = DatabaseInterface(schemas.teacher, schemas.schedule_engine, ['year'])
        self.time = DatabaseInterface(schemas.time, schemas.schedule_engine, ['id'])
        self.type = DatabaseInterface(schemas.type, schemas.schedule_engine, ['id'])
        self.weekday = DatabaseInterface(schemas.weekday, schemas.schedule_engine, ['id'])
        super().__init__(table_schema, engine, ignore_keys=['id'])

    async def _getByRowId(self, row):
        date = (await self.date.get_by_column('id',row.date_id))
        discipline = (await self.discipline.get_by_column('id', row.discipline_id))
        type = (await self.type.get_by_column('id', row.type_id))
        auditorium = (await self.auditorium.get_by_column('id', row.auditorium_id))
        teacher = (await self.teacher.get_by_column('id', row.teacher_id))
        group = (await self.group.get_by_column('id', row.group_id))
        weekday = (await self.weekday.get_by_column('id', row.weekday_id))
        return {
            "date": date[0] if date else None,  
            "discipline":discipline[0] if discipline else None,  
            "type":type[0] if type else None,  
            "auditorium":auditorium[0] if auditorium else None,  
            "teacher":teacher[0] if teacher else None,  
            "group":group[0] if group else None,  
            "weekday":weekday[0] if weekday else None  
        }

    async def get_by_row(self, row:BaseModel):
        try:
            query = self.schema.select().where(
                self.schema.c['date_id'] == row.date_id,
                self.schema.c['group_id'] == row.group_id,
                self.schema.c['teacher_id'] == row.teacher_id,
                self.schema.c['weekday_id'] == row.weekday_id,
                self.schema.c['discipline_id'] == row.discipline_id,
                self.schema.c['type_id'] == row.type_id,
                self.schema.c['auditorium_id'] == row.auditorium_id,
            )
            return self.session.execute(query).fetchone()
        except SQLException.SQLAlchemyError as error:
            raise exc.BaseAPIException(message=error.args, status_code=500)
    
    async def get(self, limit: int = 10, offset: int = 0) -> List[BaseModel]:
        data = list()
        for lesson in await super().get(limit, offset):
            data.append(await self._getByRowId(lesson))
        return data
    
    async def add(self, schedule):
        data = {
            "date_id": await self.date.select_or_add(schedule.date),
            "group_id": await self.group.select_or_add(schedule.group, key="id"),
            "teacher_id": await self.teacher.select_or_add(schedule.teacher, key="id"),
            "weekday_id": await self.weekday.select_or_add(schedule.weekday, key=None),
            "discipline_id": await self.weekday.select_or_add(schedule.discipline, key=None),
            "type_id": await self.weekday.select_or_add(schedule.type, key=None),
            "auditorium_id": await self.weekday.select_or_add(schedule.auditorium, key=None)
        }
        validated_data = self.model.parse_obj(data)
        row_of_added_data = await self.get_by_row(validated_data)
        return row_of_added_data._mapping if row_of_added_data else await super().add(validated_data)