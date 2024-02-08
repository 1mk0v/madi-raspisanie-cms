from sqlalchemy import Table, exc as SQLException
from database import DatabaseInterface, schemas
import exceptions as exc

class UserTableInterface(DatabaseInterface):
    def __init__(self, table_schema: Table = schemas.user, engine=schemas.cms_engine) -> None:
        super().__init__(table_schema, engine)


class UserInfoTableInterface(DatabaseInterface):
    def __init__(self, table_schema: Table = schemas.user_info, engine=schemas.cms_engine) -> None:
        super().__init__(table_schema, engine)

    async def get_user_type(self, id:int):
        try:
            query = schemas.user_type.select().join(
                schemas.user_type,
                self.schema.c['type_id'] == schemas.user_type.c['id']
            ).where(self.schema.c['user_id'] == id)
            return self.session.execute(query).fetchone()._mapping
        except SQLException.SQLAlchemyError as error:
            raise exc.BaseAPIException(message=error.args, status_code=500)