from database import SyncDatabaseInterface
from datetime import datetime

def get_pydantic_model(interface:SyncDatabaseInterface):
    return interface.model

def get_current_academic_year():
    current_academic_year:int = int(datetime.today().strftime("%Y"))-2000
    current_month = int(datetime.today().strftime("%m"))
    if current_month < 9:
        current_academic_year -= 1
    return current_academic_year
