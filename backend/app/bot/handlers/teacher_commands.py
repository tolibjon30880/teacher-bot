from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy import select

from app.config import TEACHER_TELEGRAM_ID
from app.database import async_session
from app.models import Group

router = Router()


def _is_teacher(message: Message) -> bool:
    return not TEACHER_TELEGRAM_ID or message.from_user.id == TEACHER_TELEGRAM_ID


@router.message(Command("newgroup"))
async def new_group(message: Message):
    if not _is_teacher(message):
        await message.answer("Bu buyruq faqat o'qituvchi uchun.")
        return

    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.answer("Foydalanish: /newgroup <guruh nomi>\nMasalan: /newgroup 9-A")
        return

    name = parts[1].strip()
    async with async_session() as session:
        group = Group(name=name)
        session.add(group)
        await session.commit()
        await session.refresh(group)

        bot_username = (await message.bot.get_me()).username
        invite_link = f"https://t.me/{bot_username}?start={group.invite_code}"

    await message.answer(
        f"✅ «{name}» guruhi yaratildi.\n\n"
        f"O'quvchilar uchun havola:\n{invite_link}\n\n"
        f"Shu havolani guruhingizga yuboring — bosishlari bilan avtomatik qo'shiladilar."
    )


@router.message(Command("groups"))
async def list_groups(message: Message):
    if not _is_teacher(message):
        return

    async with async_session() as session:
        result = await session.execute(select(Group))
        groups = result.scalars().all()

    if not groups:
        await message.answer("Hali guruh yaratilmagan. /newgroup <nomi> buyrug'idan foydalaning.")
        return

    bot_username = (await message.bot.get_me()).username
    lines = []
    for g in groups:
        link = f"https://t.me/{bot_username}?start={g.invite_code}"
        lines.append(f"• {g.name} — {link}")

    await message.answer("\n".join(lines))
