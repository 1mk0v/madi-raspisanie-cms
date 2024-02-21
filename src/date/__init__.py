from typing import List
from pydantic import BaseModel
from sqlalchemy import Engine, Table
import sqlalchemy.exc as SQLException
import exceptions as exc
from database import DatabaseInterface, schemas

class DateTableInterface(DatabaseInterface):
    def __init__(self, table_schema: Table = schemas.date, engine: Engine=schemas.schedule_engine) -> None:
        self.frequency = DatabaseInterface(schemas.frequency, schemas.schedule_engine, ['id'])
        self.time = DatabaseInterface(schemas.time, schemas.schedule_engine, ['id'])
        super().__init__(table_schema, engine, ignore_keys=["id"])

    async def _getByRowId(self, row):
        return {
            "id":row.id,
            "day":row.day,
            "frequency": (await self.frequency.get_by_column('id', row.frequency_id))[0],
            "time": (await self.time.get_by_column('id', row.time_id))[0],
        }

    async def get(self, limit: int = 10, offset: int = 0) -> List[BaseModel]:
        data = list()
        for lesson in await super().get(limit, offset):
            data.append(await self._getByRowId(lesson))
        return data
    
    async def get_by_column(self, columnName: str, value, limit: int = 10, offset: int = 0) -> List[BaseModel]:
        data = list()
        for lesson in await super().get_by_column(columnName, value, limit, offset):
            data.append(await self._getByRowId(lesson))
        return data
    
    async def __get_row(self, data):
        frequency = (await self.frequency.get_by_column('value', data.frequency))
        time = (await self.time.get_by_column('start', data.time.start))
        return {
                "day": data.day,
                "frequency_id": frequency[0].id if frequency else (await self.frequency.add(data.frequency)).id,
                "time_id": time[0].id if time else (await self.time.add(data.time)).id,
            }
    
    async def add(self, data: BaseModel):
        if data == None: return data
        try:
            finded_row = await self.get_by_row(data)
            if finded_row: return finded_row._mapping
            query = (self.schema.insert()
                     .values([data.model_dump()])
                     .returning(self.schema))
            return self.session.execute(query).fetchone()._mapping
        except SQLException.SQLAlchemyError as error:
            raise exc.BaseAPIException(message=error.args, status_code=500)
        finally:
            self.session.commit()
    

    async def get_by_row(self, row:BaseModel):
        try:
            query = self.schema.select().where(
                self.schema.c['day'] == row.day,
                self.schema.c['frequency_id'] == row.frequency_id,
                self.schema.c['time_id'] == row.time_id
            )
            return self.session.execute(query).fetchone()
        except SQLException.SQLAlchemyError as error:
            raise exc.BaseAPIException(message=error.args, status_code=500)

    async def select_or_add(self, data: dict) -> int:
        try:
            row = await self.__get_row(data)
            db_model_row = self.model(**row)
            row_of_added_data = await self.get_by_row(db_model_row)
            return row_of_added_data.id if row_of_added_data else (await self.add(db_model_row)).id
        except SQLException.SQLAlchemyError as error:
            raise exc.BaseAPIException(message=error.args, status_code=500)