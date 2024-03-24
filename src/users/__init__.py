from sqlalchemy import Table, exc as SQLException
from database import SyncDatabaseInterface
from database.schemas import cms
import exceptions as exc

class UserTableInterface(SyncDatabaseInterface):
    def __init__(self, table_schema: Table = cms.user, engine=cms.async_engine) -> None:
        super().__init__(table_schema, engine)


class UserInfoTableInterface(SyncDatabaseInterface):
    def __init__(self, table_schema: Table = cms.user_info, engine=cms.async_engine) -> None:
        super().__init__(table_schema, engine)

    async def get_user_type(self, id:int):
        try:
            query = cms.user_type.select().join(
                cms.user_type,
                self.schema.c['priority'] == cms.user_type.c['priority']
            ).where(self.schema.c['user_id'] == id)
            return await self.execute_query(query)
        except SQLException.SQLAlchemyError as error:
            raise exc.BaseAPIException(message=error.args, status_code=500)