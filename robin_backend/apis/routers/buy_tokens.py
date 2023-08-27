from fastapi import APIRouter
from pydantic import BaseModel

from database.wallet_manager import get_wallets
from on_chain.buy import Token
router = APIRouter()


class TokenForSwap(BaseModel):
    token_address:str = None
    tg_id:int
    swap_to:int = None
    swap_amount :int = None 
"""
# codes to be used as inputs into request parameters
swap for tokens = 0
swap for eth = 1
"""

@router.post("/buy")
async def swap_tokens(data:TokenForSwap):
    wallet = await get_wallets(data.tg_id)

    key = wallet[0]
    print(key.address)
    address = Token(buyer_address=key.address,token_address="0x5a0f68ffc24C4338b36a059C789B27337c5F82C3")
    balance = await address.swap_tokens_for_eth(0.5)

    print(balance)
    return balance or 0

@router.post("/get_token_balance")
async def get_token_balance(data:TokenForSwap) ->int:
    token = Token(data.token_address)
    balance = await token.get_token_balance()
    print(f"token balance : {balance}")
    return balance