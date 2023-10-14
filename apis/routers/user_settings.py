from fastapi import APIRouter
from .model_classes import User, UserSettings
from typing import Union, Dict, Optional
from database.wallet_manager import test

router = APIRouter()
"""
Get user settings
change slippage for wallet
make user premium user
ban user
scam protectoin on 
"""


@router.post("/get_settings")
async def settings(data: User):
    settings = await test(data.tg_id)
    return UserSettings(
        tg_id=data.tg_id,
        slippage=settings.slippage,
        is_premium=settings.is_premium,
        is_banned=settings.is_banned,
        enable_notifications=settings.enable_notifications,
    ).model_dump()
