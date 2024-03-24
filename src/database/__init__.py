from sqlalchemy import Table, Engine, select
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import sessionmaker
import sqlalchemy.exc as SQLException
from pydantic import BaseModel, create_model, ConfigDict, SkipValidation
import exceptions as exc
from typing import List


class SyncDatabaseInterface:

    def __init__(
            self,
            table_schema:Table,
            engine:AsyncEngine,
            ignore_keys:list = [],
            ) -> None:
        self.schema = table_schema
        self.engine = engine
        self.__dict_model = {i.name: (SkipValidation[i.type.python_type], ...) for i in self.schema.columns}
        for key in ignore_keys: self.__dict_model.pop(key, None) 
        self.__model:BaseModel = create_model(
            self.schema.name, 
            **self.__dict_model, 
            __config__=ConfigDict(arbitrary_types_allowed=True)
        )

    async def execute_query(self, query):
        try:
            async with self.engine.connect() as conn:    
                return await conn.execute(query)
        except SQLException.SQLAlchemyError as error:
            print(error)
        finally:
            await conn.close()

    async def execute_stmt(self, stmt):
        try:
            async with self.engine.connect() as conn:
                result = await conn.execute(stmt)
                await conn.commit()
                return result
        except SQLException.SQLAlchemyError as error:
            print(error)
            await conn.rollback()
        finally:
            await conn.close()

    async def get(self, limit:int = 10, offset:int = 0) -> List[BaseModel]:
        try:
            query = select(self.schema).limit(limit).offset(offset)
            return await self.execute_query(query)
        except SQLException.SQLAlchemyError as error:
            raise exc.BaseAPIException(message=error.args, status_code=500)

    async def get_by_column(self, columnName:str, value, limit:int = 10, offset:int = 0):
        try:
            query = select(self.schema).limit(limit).offset(offset).where(self.schema.c[columnName] == value)
            return await self.execute_query(query)
        except SQLException.SQLAlchemyError as error:
            raise exc.BaseAPIException(message=error.args, status_code=500)

    async def add(self, data:BaseModel):
        try:
            stmt = (self.schema.insert().values([data.model_dump()]).returning(self.schema))
            return await self.execute_stmt(stmt)
        except SQLException.SQLAlchemyError as error:
            raise exc.BaseAPIException(message=error.args, status_code=500)

    async def update(self, id, columnName, value):
        try:
            stmt = (self.schema.update().where(self.schema.c['id'] == id)
                     .values({self.schema.c[columnName]:value})
                     .execution_options(synchronize_session="fetch"))
            return await self.execute_stmt(stmt)
        except SQLException.SQLAlchemyError as error:
            raise exc.BaseAPIException(message=error.args, status_code=500)

    async def delete(self, column:str = 'id', value = None):
        try:
            stmt = (self.schema.delete().where(self.schema.c[column] == int(value))
                     .execution_options(synchronize_session="fetch")
                     .returning(self.schema))
            return await self.execute_stmt(stmt)
        except SQLException.SQLAlchemyError as error:
            raise exc.BaseAPIException(message=error.args, status_code=500)

    async def select_or_add(self, data:dict, key:str = "id") -> int:
        try:
            row = (
                await self.get_by_column(key, eval(f'data.{key}')) 
                if key else await self.get_by_column('value', data)
            )
            if row: return row[0].id
            if not key: return (await self.add(data=self.model.parse_obj({"value":data})))["id"]
            return (await self.add(data=self.model(**data)))["id"]
        finally:
            self.session.commit()

    @property
    def model(self) -> BaseModel:
        return self.__model
