from fastapi import APIRouter
from pydantic import BaseModel

from database.wallet_manager import get_wallets
from on_chain.buy import Token
router = APIRouter()


class TokenForSwap(BaseModel):
    token_address:str = None
    tg_id:int


@router.post("/buy")
async def swap_tokens(data:TokenForSwap):
    wallet = await get_wallets(data.tg_id)

    key = wallet[0]
    address = Token(buyer_address=key.address)
    balance = await address.swap_tokens_for_tokens()
    print(balance)
    return balance or 0