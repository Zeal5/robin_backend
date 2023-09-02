from fastapi import APIRouter,HTTPException
from pydantic import BaseModel
from database.wallet_manager import get_wallets

router = APIRouter()


class User(BaseModel):
    tg_id: int


@router.post("/get_wallets")
async def add_user_wallet(data: User):
    try:
        wallets = await get_wallets(data.tg_id)
        print(wallets)
        wallets_dict = {i.id: i.address for i in wallets}
        print(wallets_dict)
        return wallets_dict
    except Exception as e:
        raise HTTPException(status_code=400,detail=f"{e}")
