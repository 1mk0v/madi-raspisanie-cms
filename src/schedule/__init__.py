from sqlalchemy import Engine, Table
from database import DatabaseInterface, schemas
import datetime

class ScheduleTableInterface(DatabaseInterface):
    def __init__(self, table_schema: Table = schemas.schedule_info, engine: Engine=schemas.schedule_engine) -> None:
        self.auditorium = DatabaseInterface(schemas.auditorium, schemas.schedule_engine, ['id', 'department_id'])
        self.date = DatabaseInterface(schemas.date, schemas.schedule_engine, ['id'])
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

    #DONT WORK
    async def _get_data(self, schedule):
        data = {}
        for field in schedule:
            nameOfField = field[0]
            fieldData = field[1]
            if type(fieldData) not in [str, int, datetime.time]:
                databaseInterface:DatabaseInterface = self.__dict__[nameOfField]
                data[f'{nameOfField}_id'] = await databaseInterface.select_or_add(
                    await self._get_data(fieldData)
                )
            else:
                if nameOfField in ['frequency']:
                    databaseInterface:DatabaseInterface = self.__dict__[nameOfField]
                    data[f'{nameOfField}_id'] = await databaseInterface.select_or_add({'value':fieldData})
                else:
                    data[f'{nameOfField}'] = fieldData
        return data
    
    async def add(self, schedule):
        data = await self._get_data(schedule)
        new_data = dict()
        for key in data:
            if type(data[key]) == str:
                databaseInterface:DatabaseInterface = self.__dict__[key]
                new_data[f'{key}_id'] = await databaseInterface.select_or_add({'value':data[key]})
            else:
                new_data[key] = data[key]
        return await super().add(self.model(**new_data))