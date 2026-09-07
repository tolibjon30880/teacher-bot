import datetime
from pydantic import BaseModel, ConfigDict


class GroupOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    invite_code: str


class GroupCreate(BaseModel):
    name: str


class StudentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    full_name: str
    username: str | None
    group_id: int


class ScheduleEntryCreate(BaseModel):
    weekday: int  # 0=Dushanba ... 6=Yakshanba
    time: str


class ScheduleEntryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    weekday: int
    time: str


class LessonOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    group_id: int
    date: datetime.date
    time: str
    status: str


class AttendanceUpdate(BaseModel):
    student_id: int
    present: bool
    homework_done: bool | None = None
    score: float | None = None
    note: str | None = None


class AttendanceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    student_id: int
    present: bool
    homework_done: bool | None
    score: float | None
    note: str | None


class StudentStatsOut(BaseModel):
    student_id: int
    full_name: str
    average_score: float | None
    total_lessons: int
    attended: int
    missed: int
    attendance_rate: float
    history: list["LessonHistoryItem"]


class LessonHistoryItem(BaseModel):
    date: datetime.date
    present: bool
    homework_done: bool | None
    score: float | None
    note: str | None
