import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import TEACHER_TELEGRAM_ID
from app.database import get_session
from app.models import Group, Student, ScheduleEntry, Lesson, LessonStatus, Attendance
from app.schemas.schemas import (
    GroupOut, GroupCreate, StudentOut, ScheduleEntryCreate, ScheduleEntryOut,
    LessonOut, AttendanceUpdate, AttendanceOut,
)
from app.telegram_auth import get_current_telegram_user

router = APIRouter(prefix="/api/teacher", tags=["teacher"])


def _ensure_teacher(user: dict):
    if TEACHER_TELEGRAM_ID and user["id"] != TEACHER_TELEGRAM_ID:
        raise HTTPException(status_code=403, detail="Faqat o'qituvchi uchun")


@router.get("/groups", response_model=list[GroupOut])
async def list_groups(
    user: dict = Depends(get_current_telegram_user),
    session: AsyncSession = Depends(get_session),
):
    _ensure_teacher(user)
    result = await session.execute(select(Group))
    return result.scalars().all()


@router.post("/groups", response_model=GroupOut)
async def create_group(
    payload: GroupCreate,
    user: dict = Depends(get_current_telegram_user),
    session: AsyncSession = Depends(get_session),
):
    _ensure_teacher(user)
    group = Group(name=payload.name)
    session.add(group)
    await session.commit()
    await session.refresh(group)
    return group


@router.get("/groups/{group_id}/students", response_model=list[StudentOut])
async def list_students(
    group_id: int,
    user: dict = Depends(get_current_telegram_user),
    session: AsyncSession = Depends(get_session),
):
    _ensure_teacher(user)
    result = await session.execute(select(Student).where(Student.group_id == group_id))
    return result.scalars().all()


@router.post("/groups/{group_id}/schedule", response_model=ScheduleEntryOut)
async def add_schedule_entry(
    group_id: int,
    payload: ScheduleEntryCreate,
    user: dict = Depends(get_current_telegram_user),
    session: AsyncSession = Depends(get_session),
):
    _ensure_teacher(user)
    entry = ScheduleEntry(group_id=group_id, weekday=payload.weekday, time=payload.time)
    session.add(entry)
    await session.commit()
    await session.refresh(entry)
    return entry


@router.get("/groups/{group_id}/schedule", response_model=list[ScheduleEntryOut])
async def get_schedule(
    group_id: int,
    user: dict = Depends(get_current_telegram_user),
    session: AsyncSession = Depends(get_session),
):
    _ensure_teacher(user)
    result = await session.execute(
        select(ScheduleEntry).where(ScheduleEntry.group_id == group_id)
    )
    return result.scalars().all()


@router.get("/lessons/today", response_model=list[LessonOut])
async def todays_lessons(
    user: dict = Depends(get_current_telegram_user),
    session: AsyncSession = Depends(get_session),
):
    """Bugungi jadval asosida darslarni topadi, agar bazada bo'lmasa yaratadi."""
    _ensure_teacher(user)
    today = datetime.date.today()
    weekday = today.weekday()  # 0=Dushanba

    result = await session.execute(
        select(ScheduleEntry).where(ScheduleEntry.weekday == weekday)
    )
    entries = result.scalars().all()

    lessons = []
    for entry in entries:
        existing = await session.execute(
            select(Lesson).where(
                Lesson.group_id == entry.group_id,
                Lesson.date == today,
                Lesson.time == entry.time,
            )
        )
        lesson = existing.scalar_one_or_none()
        if not lesson:
            lesson = Lesson(
                group_id=entry.group_id, date=today, time=entry.time,
                status=LessonStatus.PENDING,
            )
            session.add(lesson)
            await session.commit()
            await session.refresh(lesson)
        lessons.append(lesson)

    return lessons


@router.post("/lessons/{lesson_id}/status")
async def set_lesson_status(
    lesson_id: int,
    status: LessonStatus,
    user: dict = Depends(get_current_telegram_user),
    session: AsyncSession = Depends(get_session),
):
    _ensure_teacher(user)
    lesson = await session.get(Lesson, lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Dars topilmadi")
    lesson.status = status
    await session.commit()
    return {"ok": True, "status": lesson.status}


@router.post("/lessons/{lesson_id}/attendance", response_model=list[AttendanceOut])
async def submit_attendance(
    lesson_id: int,
    records: list[AttendanceUpdate],
    user: dict = Depends(get_current_telegram_user),
    session: AsyncSession = Depends(get_session),
):
    _ensure_teacher(user)
    lesson = await session.get(Lesson, lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Dars topilmadi")

    saved = []
    for rec in records:
        existing = await session.execute(
            select(Attendance).where(
                Attendance.lesson_id == lesson_id,
                Attendance.student_id == rec.student_id,
            )
        )
        attendance = existing.scalar_one_or_none()
        if not attendance:
            attendance = Attendance(lesson_id=lesson_id, student_id=rec.student_id)
            session.add(attendance)

        attendance.present = rec.present
        attendance.homework_done = rec.homework_done
        attendance.score = rec.score
        attendance.note = rec.note
        saved.append(attendance)

    await session.commit()
    for a in saved:
        await session.refresh(a)
    return saved
