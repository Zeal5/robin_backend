from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, validator
import json
from .helpers.formate_balance import format_number
from .helpers.token_swaps import Swap

# from database.wallet_manager import get_active_wallet,get_slippage
from .helpers.wallet_factory import WalletFactory
router = APIRouter()


weth_address = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
dai_address = "0x6B175474E89094C44Da98b954EedeAC495271d0F"
usdt = "0xdAC17F958D2ee523a2206206994597C13D831ec7"


class TokenForSwap(BaseModel):
    tg_id: int
    token_to_buy: str | None = None
    token_to_sell: str | None = None

    # amount_to_buy: int | None = None
    eth_to_spend: float | str | None = None
    token_amount_to_sell: float | None = None
    
    slippage: float | None = None

    @validator("eth_to_spend", always=False)
    def check_if_eth_to_spend_is_less_then_0(cls, value):
        if value is not None and value == 0:
            raise HTTPException(
                status_code=400, detail=f"eth amount to spend can not be 0"
            )
        elif value is not None and value < 0:
            raise HTTPException(
                status_code=400, detail=f"eth amount to spend can not be less then 0"
            )
        return value

    # @TODO create validator for each property of pydantic class to validate inputs are not 0
    @validator("token_amount_to_sell", always=False)
    def check_if_token_amount_to_sell_is_less_then_0(cls, value):
        if value is not None and value == 0:
            raise HTTPException(status_code=400, detail=f"amount to spend can not be 0")
        elif value is not None and value < 0:
            raise HTTPException(
                status_code=400, detail=f"amount to spend can not be less then 0"
            )
        return value


# @ TODO in front end make making reqqest to serevr modular
# @ TODO change function later to implement actual buy sell
@router.post("/buy_tokens_with_eth")
async def buy_tokens_with_eth(data: TokenForSwap):

    print(f"eth to spend = {data.eth_to_spend}")
    if data.eth_to_spend is None:
        raise HTTPException(status_code=400, detail="No eth amount specified")
    try:
        wallet: dict = await WalletFactory(data.tg_id).get_wallet()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"No Wallets found")

    try:
        buy = Swap(
            token_to_buy=data.token_to_buy,
            buyer_address=wallet["wallet_address"],
            buyer_secret=wallet["wallet_secret"],
        )
    except ValueError as value_error:
        exception = str(value_error).split("'")[1]
        raise HTTPException(status_code=400, detail=f"address ({exception}) is invalid")
    except Exception as e:
        print(e)
        return {
            "error": e
        }  # HTTPException(status_code=400, detail="one of the addresses is invalid")

    try:
        print(data.eth_to_spend)
        print(f"eth to spend buy_token {type(data.eth_to_spend)}")
        buying = await buy.buy(eth_to_spend=data.eth_to_spend)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"'error' : {e}")
    print(f"buying => {buying}")
    if buying.get("detail"):
        err = buying["detail"]
        buying["detail"] = (
            err
            + f"\nFor {wallet['wallet_name']} ({wallet['wallet_address']})\nto change active wallet use `/manage_wallets`"
        )
    return buying

    # @TODO return eth balance and token amount balance too


@router.post("/swap")
async def swap_tokens(data: TokenForSwap):
    pass


@router.post("/sell_into_eth")
async def swap_tokens(data: TokenForSwap):
    if data.token_amount_to_sell is None:
        raise HTTPException(status_code=400, detail="No amount to sell specifie")
    if data.token_to_sell is None:
        raise HTTPException(
            status_code=400, detail="No amount of token to sell specified"
        )

    wallet: dict = await WalletFactory(data.tg_id).get_wallet()

