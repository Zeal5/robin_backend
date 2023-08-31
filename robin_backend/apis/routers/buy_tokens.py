from fastapi import APIRouter
from pydantic import BaseModel
import json
from routers.helpers.formate_balance import format_number
from database.wallet_manager import get_wallets
from on_chain.buy import Token
router = APIRouter()


weth_address = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
dai_address = "0x6B175474E89094C44Da98b954EedeAC495271d0F"
usdt = "0xdAC17F958D2ee523a2206206994597C13D831ec7"

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
#@TODO change function later to implement actual buy sell
@router.post("/buy")
async def swap_tokens(data:TokenForSwap):
    # wallet = await get_wallets(data.tg_id)

    # key = wallet[0]
    # print(key.address)
    address = Token(buyer_address="0x136be469A3203D20a853a546Af89867AE4B437b9",
                    buyer_secret="0xc55c8750c851c723e36485856c96760f33efb7b3b281e9a0ecf674f3070f0939",
                    token_to_sell=dai_address,
                    token_to_buy=usdt,
                    )
    
    # balance = await address.swap_tokens_for_eth(1731.17)

    # balance = await address.swap_tokens_for_tokens(100)
    # balance = await address.swap_eth_for_tokens(0.1)
    balance = await address.swap_tokens_for_eth(800000)

    print(balance)
    return (balance)

@router.post("/get_token_balance")
async def get_token_balance(data:TokenForSwap):
    # token = Token(data.token_address)
    
    address = Token(buyer_address="0x136be469A3203D20a853a546Af89867AE4B437b9",
                    token_address_for_info=weth_address)
    balance = await address.get_token_balance()
    print(f"token balance : {format_number(balance)}")
    return f"{format_number(balance)}"
    
    # usdt = Token(token_address_for_info="0x6B175474E89094C44Da98b954EedeAC495271d0F")
    # decimal = await usdt._get_decimals()

    # print(decimal)
    # return decimal