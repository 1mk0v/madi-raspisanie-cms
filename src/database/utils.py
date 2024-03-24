from sqlalchemy import Table, inspect
from typing import Dict

def get_tables(engine, metadata) -> Dict[str, Table]:
    inspector = inspect(engine)
    table_names = inspector.get_table_names()
    tables_info = dict()
    for table_name in table_names:
        tables_info[table_name] = Table(table_name, metadata, autoload_with=engine)
    return tables_info

def get_db_url(db_driver ,user, password, host, name):
    return f"postgresql+{db_driver}://{user}:{password}@{host}/{name}"