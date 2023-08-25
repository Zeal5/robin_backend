from fastapi import APIRouter
from pydantic import BaseModel
from database.wallet_manager import get_wallets

router = APIRouter()


class User(BaseModel):
    tg_id: int


@router.post("/get_wallets")
async def add_user_wallet(data: User):
    wallets = await get_wallets(data.tg_id)
    wallets_dict = {i.id: i.address for i in wallets}
    return wallets_dict
