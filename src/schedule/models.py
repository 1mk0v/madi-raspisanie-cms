from pydantic import BaseModel
import datetime
from typing import List


class Essence(BaseModel):
    id:int | None = None
    value:str | None = None

class Community(Essence):
    department_id:int | None = None

class Time(BaseModel):
    start:datetime.time | None = None
    end:datetime.time | None = None

class Date(BaseModel):
    day:str | None = None
    friequency: str | None = None
    time:Time | None = None

class Lesson(BaseModel):
    date:Date | None = None
    discipline:str | List = None
    type:str | None = None
    auditorium:str | None = None

class Schedule(Lesson):
    group:Community | None = None
    teacher:Community | None = None

class LessonInfo(Schedule):
    weekday:str | None = None
