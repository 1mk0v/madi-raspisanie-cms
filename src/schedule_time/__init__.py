
from pydantic import BaseModel
from sqlalchemy import Engine, Table
import sqlalchemy.exc as SQLException
import exceptions as exc
from database import DatabaseInterface, schemas
import datetime, time

class TimeTableInterface(DatabaseInterface):
    def __init__(self, table_schema: Table = schemas.time, engine: Engine = schemas.schedule_engine,
                 ignore_keys=["id"]) -> None:
        super().__init__(table_schema, engine, ignore_keys)

    
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
                self.schema.c['start'] == datetime.datetime.strptime(row.start, "%H:%M:%S.%fZ").time(),
                self.schema.c['end'] == datetime.datetime.strptime(row.end, "%H:%M:%S.%fZ").time()
            )
            return self.session.execute(query).fetchone()
        except SQLException.SQLAlchemyError as error:
            raise exc.BaseAPIException(message=error.args, status_code=500)