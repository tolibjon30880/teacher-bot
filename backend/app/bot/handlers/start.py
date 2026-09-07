from aiogram import Router, F
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import select

from app.config import MINI_APP_URL, TEACHER_TELEGRAM_ID
from app.database import async_session
from app.models import Group, Student

router = Router()


@router.message(CommandStart(deep_link=True))
async def start_with_invite(message: Message, command: CommandObject):
    """O'quvchi guruh linki orqali kirganda: /start <invite_code>"""
    invite_code = command.args

    async with async_session() as session:
        result = await session.execute(
            select(Group).where(Group.invite_code == invite_code)
        )
        group = result.scalar_one_or_none()

        if not group:
            await message.answer(
                "❌ Bu havola noto'g'ri yoki eskirgan. "
                "O'qituvchingizdan yangi havola so'rang."
            )
            return

        existing = await session.execute(
            select(Student).where(Student.telegram_id == message.from_user.id)
        )
        student = existing.scalar_one_or_none()

        if student:
            student.group_id = group.id
            await session.commit()
            await message.answer(f"✅ Siz «{group.name}» guruhiga o'tkazildingiz.")
        else:
            student = Student(
                telegram_id=message.from_user.id,
                full_name=message.from_user.full_name,
                username=message.from_user.username,
                group_id=group.id,
            )
            session.add(student)
            await session.commit()
            await message.answer(
                f"✅ Xush kelibsiz! Siz «{group.name}» guruhiga qo'shildingiz."
            )

    await _send_mini_app_button(message)


@router.message(CommandStart())
async def start_plain(message: Message):
    """Oddiy /start — havolasiz kirgan holat."""
    if TEACHER_TELEGRAM_ID and message.from_user.id == TEACHER_TELEGRAM_ID:
        await message.answer(
            "👋 Salom, ustoz! Boshqaruv panelini ochish uchun quyidagi tugmani bosing."
        )
    else:
        await message.answer(
            "👋 Salom! Guruhga qo'shilish uchun o'qituvchingizdan "
            "taklif havolasini so'rang."
        )
    await _send_mini_app_button(message)


async def _send_mini_app_button(message: Message):
    kb = InlineKeyboardBuilder()
    kb.button(text="📱 Kabinetni ochish", web_app=WebAppInfo(url=MINI_APP_URL))
    await message.answer("Shaxsiy kabinet:", reply_markup=kb.as_markup())
