"""
Telegram Mini App initData'ni tekshirish (xavfsizlik uchun majburiy).
https://core.teleg  ram.org/bots/webapps#validating-data-received-via-the-mini-app
"""
import hashlib
import hmac
import json
from urllib.parse import parse_qsl

from fastapi import Header, HTTPException

from app.config import BOT_TOKEN


def validate_init_data(init_data: str) -> dict:
    """initData'ni tekshiradi va foydalanuvchi ma'lumotini qaytaradi."""
    try:
        parsed = dict(parse_qsl(init_data, strict_parsing=True))
    except ValueError:
        raise HTTPException(status_code=401, detail="Noto'g'ri initData")

    received_hash = parsed.pop("hash", None)
    if not received_hash:
        raise HTTPException(status_code=401, detail="Hash topilmadi")

    data_check_string = "\n".join(
        f"{k}={v}" for k, v in sorted(parsed.items())
    )
    secret_key = hmac.new(
        b"WebAppData", BOT_TOKEN.encode(), hashlib.sha256
    ).digest()
    calculated_hash = hmac.new(
        secret_key, data_check_string.encode(), hashlib.sha256
    ).hexdigest()

    if calculated_hash != received_hash:
        raise HTTPException(status_code=401, detail="Autentifikatsiya xato")

    user_json = parsed.get("user")
    if not user_json:
        raise HTTPException(status_code=401, detail="Foydalanuvchi topilmadi")

    return json.loads(user_json)


async def get_current_telegram_user(
    x_telegram_init_data: str = Header(..., alias="X-Telegram-Init-Data")
) -> dict:
    """FastAPI dependency: har bir himoyalangan endpoint uchun."""
    return validate_init_data(x_telegram_init_data)
