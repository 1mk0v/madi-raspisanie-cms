from fastapi import Query
from typing import Annotated
from utils import get_current_academic_year

def current_year(year:Annotated[int, Query(ge = 19, le = get_current_academic_year()+1)] = get_current_academic_year()):
    return year
