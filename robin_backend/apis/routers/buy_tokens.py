from fastapi import APIRouter, HTTPException
from pydantic import BaseModel,validator 
import json
from .helpers.formate_balance import format_number
from .helpers.address_checker import Swap

from database.wallet_manager import get_wallets
from on_chain.buy import Token

router = APIRouter()


weth_address = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
dai_address = "0x6B175474E89094C44Da98b954EedeAC495271d0F"
usdt = "0xdAC17F958D2ee523a2206206994597C13D831ec7"

      
class TokenForSwap(BaseModel):
    tg_id: int
    token_to_buy: str | None = None
    token_to_sell: str | None = None
    # amount_to_buy: int | None = None
    eth_to_spend: float | None = None
    amount_to_sell: float | None = None
    slippage: float | None = None


    @validator("eth_to_spend", always=True)
    def check_if_eth_to_spend_is_less_then_0(cls, value):
        if value is not None and value <= 0:
           HTTPException(status_code=400, detail=f"eth amount to spend can not be 0")
        return value

    #@TODO create validator for each property of pydantic class to validate inputs are not 0
    @validator("amount_to_sell", always=True)
    def check_if_token_amount_to_sell_is_less_then_0(cls, value):
        if value is not None and value <= 0:
           HTTPException(status_code=400, detail=f"amount to spend can not be 0")
        return value

"""
# codes to be used as inputs into request parameters
swap for tokens = 0
swap for eth = 1
"""


@router.post("/sell_into_eth")
async def swap_tokens(data: TokenForSwap):
    pass


# @TODO change function later to implement actual buy sell
@router.post("/buy_tokens_with_eth")
async def buy_tokens_with_eth(data: TokenForSwap):

    try:
        buy = Swap(
            token_to_buy=data.token_to_buy,
            buyer_address="0x136be469A3203D20a853a546Af89867AE4B437b9",
            buyer_secret="0xc55c8750c851c723e36485856c96760f33efb7b3b281e9a0ecf674f3070f0939",
        )  # data.token_to_buy)
    except ValueError as value_error:
        exception = str(value_error).split("'")[1]
        raise HTTPException(status_code=400, detail=f"address ({exception}) is invalid")
    except Exception as e:
        print(e)
        return {'error': e}  # HTTPException(status_code=400, detail="one of the addresses is invalid")

    try:
        print(data.eth_to_spend)
        print(f"eth to spend buy_token {type(data.eth_to_spend)}")
        buying = await buy.buy(eth_to_spend=data.eth_to_spend)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"'error' : {e}")
    print(f"buying => {buying}")
    return buying

    #@TODO return eth balance and token amount balance too

    # print(f"type of tg_id {type(data.tg_id)}")
    # print(f"type of buy token {type(data.token_to_buy)}")
    # print(f"type of sell token {type(data.token_to_sell)}")
    # print(f"type of eth to spend {type(data.eth_to_spend)}")
    # print(f"type of amount to sell {type(data.amount_to_sell)}")
    # print(f"type of slippage {type(data.slippage)}")

    # wallet = await get_wallets(data.tg_id)

    # key = wallet[0]
    # print(key.address)
    # address = Token(buyer_address="0x136be469A3203D20a853a546Af89867AE4B437b9",
    #                 buyer_secret="0xc55c8750c851c723e36485856c96760f33efb7b3b281e9a0ecf674f3070f0939",
    #                 token_to_sell=dai_address,
    #                 token_to_buy=usdt,
    #                 )

    # balance = await address.swap_tokens_for_eth(1731.17)

    # balance = await address.swap_tokens_for_tokens(100)
    # balance = await address.swap_eth_for_tokens(0.1)
    # balance = await address.swap_tokens_for_eth(800000)

    # print(balance)
    # return (balance)


@router.post("/swap")
async def swap_tokens(data: TokenForSwap):
    pass


@router.post("/get_token_balance")
async def get_token_balance(data: TokenForSwap):
    # token = Token(data.token_address)

    address = Token(
        buyer_address="0x136be469A3203D20a853a546Af89867AE4B437b9",
        token_address_for_info=weth_address,
    )
    balance = await address._get_token_balance()
    print(f"token balance : {format_number(balance)}")
    return f"{format_number(balance)}"

    # usdt = Token(token_address_for_info="0x6B175474E89094C44Da98b954EedeAC495271d0F")
    # decimal = await usdt._get_decimals()

    # print(decimal)
    # return decimal
