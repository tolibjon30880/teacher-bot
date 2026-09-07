import datetime
import enum
import secrets

from sqlalchemy import (
    String, Integer, ForeignKey, DateTime, Date, Boolean, Enum, Float
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


def gen_invite_code() -> str:
    return secrets.token_urlsafe(6)


class Group(Base):
    """Guruh = sinf/klass — birga o'qiydigan o'quvchilar to'plami."""
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    invite_code: Mapped[str] = mapped_column(
        String(20), unique=True, default=gen_invite_code
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.utcnow
    )

    students: Mapped[list["Student"]] = relationship(
        back_populates="group", cascade="all, delete-orphan"
    )
    schedule_entries: Mapped[list["ScheduleEntry"]] = relationship(
        back_populates="group", cascade="all, delete-orphan"
    )
    lessons: Mapped[list["Lesson"]] = relationship(
        back_populates="group", cascade="all, delete-orphan"
    )


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(150))
    username: Mapped[str | None] = mapped_column(String(100), nullable=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))
    joined_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.utcnow
    )

    group: Mapped["Group"] = relationship(back_populates="students")
    attendance_records: Mapped[list["Attendance"]] = relationship(
        back_populates="student", cascade="all, delete-orphan"
    )


class Weekday(enum.IntEnum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


class ScheduleEntry(Base):
    """Guruh uchun haftalik dars jadvali (masalan: Dushanba 14:00)."""
    __tablename__ = "schedule_entries"

    id: Mapped[int] = mapped_column(primary_key=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))
    weekday: Mapped[int] = mapped_column(Integer)  # 0=Dushanba ... 6=Yakshanba
    time: Mapped[str] = mapped_column(String(5))  # "14:00"

    group: Mapped["Group"] = relationship(back_populates="schedule_entries")


class LessonStatus(str, enum.Enum):
    PENDING = "pending"       # hali belgilanmagan
    HELD = "held"              # o'tdi
    CANCELLED = "cancelled"    # bekor qilindi


class Lesson(Base):
    """Muayyan sanadagi bitta dars (jadvaldan avtomatik yaratiladi)."""
    __tablename__ = "lessons"

    id: Mapped[int] = mapped_column(primary_key=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))
    date: Mapped[datetime.date] = mapped_column(Date)
    time: Mapped[str] = mapped_column(String(5))
    status: Mapped[LessonStatus] = mapped_column(
        Enum(LessonStatus), default=LessonStatus.PENDING
    )

    group: Mapped["Group"] = relationship(back_populates="lessons")
    attendance_records: Mapped[list["Attendance"]] = relationship(
        back_populates="lesson", cascade="all, delete-orphan"
    )


class Attendance(Base):
    """Bitta o'quvchining bitta darsdagi natijasi."""
    __tablename__ = "attendance"

    id: Mapped[int] = mapped_column(primary_key=True)
    lesson_id: Mapped[int] = mapped_column(ForeignKey("lessons.id"))
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))

    present: Mapped[bool] = mapped_column(Boolean, default=True)
    homework_done: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    score: Mapped[float | None] = mapped_column(Float, nullable=True)  # 0-100
    note: Mapped[str | None] = mapped_column(String(300), nullable=True)

    lesson: Mapped["Lesson"] = relationship(back_populates="attendance_records")
    student: Mapped["Student"] = relationship(back_populates="attendance_records")
