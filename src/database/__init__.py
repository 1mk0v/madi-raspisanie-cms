from sqlalchemy import Table, Engine
from sqlalchemy.orm import sessionmaker
import sqlalchemy.exc as SQLException
from pydantic import BaseModel, create_model, ConfigDict, SkipValidation
import exceptions as exc
from typing import List


class DatabaseInterface:

    def __init__(
            self,
            table_schema:Table,
            engine:Engine,
            ignore_keys:list = [],
            ) -> None:
        self.schema = table_schema
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.__dict_model = {i.name: (SkipValidation[i.type.python_type], ...) for i in self.schema.columns}
        for key in ignore_keys: self.__dict_model.pop(key, None) 
        self.__model:BaseModel = create_model(
            self.schema.name, 
            **self.__dict_model, 
            __config__=ConfigDict(arbitrary_types_allowed=True)
        )

    async def get(self, limit:int = 10, offset:int = 0) -> List[BaseModel]:
        try:
            query = self.schema.select().limit(limit).offset(offset)
            return [i._mapping for i in self.session.execute(query).all()]
        except SQLException.SQLAlchemyError as error:
            raise exc.BaseAPIException(message=error.args, status_code=500)

    async def get_by_column(self, columnName:str, value, limit:int = 10, offset:int = 0) -> List[BaseModel]:
        try:
            query = self.schema.select().limit(limit).offset(offset).where(self.schema.c[columnName] == value)
            return [i._mapping for i in self.session.execute(query).all()]
        except SQLException.SQLAlchemyError as error:
            raise exc.BaseAPIException(message=error.args, status_code=500)

    async def add(self, data:BaseModel):
        if data == None: return data
        try:
            query = (self.schema.insert()
                     .values([data.model_dump()])
                     .returning(self.schema))
            return self.session.execute(query).fetchone()._mapping
        except SQLException.SQLAlchemyError as error:
            raise exc.BaseAPIException(message=error.args, status_code=500)
        finally:
            self.session.commit()

    async def update(self, id, columnName, value):
        try:
            query = (self.schema.update().where(self.schema.c['id'] == id)
                     .values({self.schema.c[columnName]:value})
                     .execution_options(synchronize_session="fetch"))
            return self.session.execute(query)
        except SQLException.SQLAlchemyError as error:
            raise exc.BaseAPIException(message=error.args, status_code=500)
        finally:
            self.session.commit()

    async def delete(self, column:str = 'id', value = None):
        try:
            query = (self.schema.delete().where(self.schema.c[column] == int(value))
                     .execution_options(synchronize_session="fetch")
                     .returning(self.schema))
            return self.session.execute(query).rowcount
        except SQLException.SQLAlchemyError as error:
            raise exc.BaseAPIException(message=error.args, status_code=500)
        finally:
            self.session.commit()

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
