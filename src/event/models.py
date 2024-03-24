from pydantic import BaseModel
from community.router import CommunityModel
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

class Lesson(BaseModel):
    date:str | None = None
    time:Time | None = None
    frequency: str | None = None
    discipline:str | List = None
    type:str | None = None
    auditorium:str | None = None

class Schedule(Lesson):
    group:CommunityModel | None = None # type: ignore
    teacher:CommunityModel | None = None # type: ignore

class LessonInfo(Schedule):
    weekday:str | None = None

    class Config():
        pass

class GetScheduleModel(BaseModel):
    id:int
    date:str | None = None
    time:Time | None = None
    frequency: str | None = None
    discipline:Essence | None = None 
    type:Essence | None = None
    auditorium:Community | None = None
    group:CommunityModel | None = None # type: ignore
    teacher:CommunityModel | None = None # type: ignore
    weekday:Essence | None = None