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
            engine:Engine
            ) -> None:
        self.schema = table_schema
        Session = sessionmaker(bind=engine)
        self.session = Session()
        model = {i.name: (SkipValidation[i.type.python_type], ...) for i in self.schema.columns}
        config = ConfigDict(arbitrary_types_allowed=True)
        self.__model:BaseModel = create_model(self.schema.name, **model, __config__=config)

    async def get(self, limit:int = 10, offset:int = 0) -> List[BaseModel]:
        try:
            query = self.schema.select().limit(limit).offset(offset)
            return [self.__model(**i._mapping) for i in self.session.execute(query).all()]
        except SQLException.SQLAlchemyError as error:
            raise exc.BaseAPIException(message=error.args, status_code=500)

    async def get_by_column(self, columnName:str, value, limit:int = 10, offset:int = 0) -> List[BaseModel]:
        try:
            query = self.schema.select().limit(limit).offset(offset).where(self.schema.c[columnName] == value)
            return [self.__model(**i._mapping) for i in self.session.execute(query).all()]
        except SQLException.SQLAlchemyError as error:
            raise exc.BaseAPIException(message=error.args, status_code=500)

    async def add(self, data:BaseModel | List[BaseModel]):
        try:
            query = (self.schema.insert()
                     .values([data.model_dump()])
                     .returning(self.schema))
            return self.session.execute(query).fetchall()
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

    @property
    def model(self) -> BaseModel:
        return self.__model
