from sqlalchemy import Engine, Table
from database import DatabaseInterface, schemas
import datetime
from pydantic import BaseModel

class ScheduleTableInterface(DatabaseInterface):
    def __init__(self, table_schema: Table = schemas.schedule_info, engine: Engine=schemas.schedule_engine) -> None:
        self.auditorium = DatabaseInterface(schemas.auditorium, schemas.schedule_engine)
        self.date = DatabaseInterface(schemas.date, schemas.schedule_engine)
        self.department = DatabaseInterface(schemas.department, schemas.schedule_engine)
        self.discipline = DatabaseInterface(schemas.discipline, schemas.schedule_engine)
        self.exam_info = DatabaseInterface(schemas.exam_info, schemas.schedule_engine)
        self.frequency = DatabaseInterface(schemas.frequency, schemas.schedule_engine)
        self.group = DatabaseInterface(schemas.group, schemas.schedule_engine)
        self.teacher = DatabaseInterface(schemas.teacher, schemas.schedule_engine)
        self.time = DatabaseInterface(schemas.time, schemas.schedule_engine)
        self.type = DatabaseInterface(schemas.type, schemas.schedule_engine)
        self.weekday = DatabaseInterface(schemas.weekday, schemas.schedule_engine)
        super().__init__(table_schema, engine)

    #DONT WORK
    async def add(self, schedule):
        data = {}
        for field in schedule:
            nameOfField = field[0]
            fieldData = field[1]
            if type(fieldData) not in [str, int, datetime.time]:
                print(data)
                databaseInterface:DatabaseInterface = self.__dict__[nameOfField] 
                data[f'{nameOfField}_id'] = await databaseInterface.add(
                    databaseInterface.model(
                        (await self.add(field)).id
                    )
                ) 
            else:
                data[f'{nameOfField}'] = fieldData
        
        
        return data
        
            # databaseInterface:DatabaseInterface = self.__dict__[nameOfField]
                # print(databaseInterface.model)
            # data[f'{nameOfField}_id'] = await databaseInterface.add(fieldData)
        # query = self.schema.insert().values(data)