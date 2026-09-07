import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./teacher_bot.db")
MINI_APP_URL = os.getenv("MINI_APP_URL", "https://example.com")
TEACHER_TELEGRAM_ID = int(os.getenv("TEACHER_TELEGRAM_ID", "0"))
