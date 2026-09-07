from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models import Student, Attendance, Lesson
from app.schemas.schemas import StudentStatsOut, LessonHistoryItem
from app.telegram_auth import get_current_telegram_user

router = APIRouter(prefix="/api/student", tags=["student"])


@router.get("/stats", response_model=StudentStatsOut)
async def my_stats(
    user: dict = Depends(get_current_telegram_user),
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(
        select(Student).where(Student.telegram_id == user["id"])
    )
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(
            status_code=404,
            detail="Siz hali hech qaysi guruhga qo'shilmagansiz",
        )

    result = await session.execute(
        select(Attendance, Lesson)
        .join(Lesson, Attendance.lesson_id == Lesson.id)
        .where(Attendance.student_id == student.id)
        .order_by(Lesson.date.desc())
    )
    rows = result.all()

    scores = [a.score for a, _ in rows if a.score is not None]
    attended = sum(1 for a, _ in rows if a.present)
    missed = sum(1 for a, _ in rows if not a.present)
    total = len(rows)

    history = [
        LessonHistoryItem(
            date=lesson.date,
            present=att.present,
            homework_done=att.homework_done,
            score=att.score,
            note=att.note,
        )
        for att, lesson in rows
    ]

    return StudentStatsOut(
        student_id=student.id,
        full_name=student.full_name,
        average_score=(sum(scores) / len(scores)) if scores else None,
        total_lessons=total,
        attended=attended,
        missed=missed,
        attendance_rate=(attended / total * 100) if total else 0.0,
        history=history,
    )
