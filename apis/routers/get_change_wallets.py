from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database.wallet_manager import get_wallets, get_active_wallets_id, change_active_wallet
from fastapi.responses import JSONResponse
router = APIRouter()


class User(BaseModel):
    tg_id: int
    button_id: int = None


@router.post("/get_wallets")
async def get_user_wallet(data: User):
    try:
        wallets = await get_wallets(data.tg_id)
        active_wallet_id = await get_active_wallets_id(data.tg_id)
        print(wallets)
        # wallets_dict = [{"id": i.id, "wallet_address": f"{i.address}", "wallet_name":i.name} for i in wallets]
        wallets_dict = []
        for wallet in wallets:
            if wallet.id == active_wallet_id:
                wallets_dict.append(
                    {
                        "id": wallet.id,
                        "address": f"{wallet.address}",
                        "wallet_name": wallet.name,
                        "is_active": True,
                    }
                )
            else:
                wallets_dict.append(
                {
                    "id": wallet.id,
                    "address": f"{wallet.address}",
                    "wallet_name": wallet.name,
                    "is_active": False,
                }
            )

        print(wallets_dict)
        return wallets_dict

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")


@router.patch("/change_active_wallet")
async def change_active_wallet_funtion(data: User):
    wallet_changed = await change_active_wallet(data.tg_id, data.button_id)
    if wallet_changed:
        return JSONResponse(content=wallet_changed)
    else:
        print("error updating active wallet")
        raise HTTPException(status_code=400, detail="could not update wallet")

# @router.patch("change_slippage")
# async def
