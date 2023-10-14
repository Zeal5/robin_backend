from on_chain.buy import Token
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from .helpers.formate_balance import format_number
from .helpers.wallet_factory import WalletFactory
from .helpers.token_swaps import Swap
from .helpers.etherscan_functions import GetBalances

router = APIRouter()


class TokenBalance(BaseModel):
    tg_id: int
    token_address: str | None = None


@router.get("/get_token_balance")
async def get_token_balance(data: TokenBalance):
    print(f"token address = {data.token_address}")
    try:
        wallet: dict = await WalletFactory(data.tg_id).get_wallet()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"No Wallets found")
    user_address = wallet["wallet_address"]
    print(data.tg_id)
    print(type(data.tg_id))
    balance: dict = await GetBalances().get_token_balance(
        token_address=data.token_address,
        user_address=user_address,
    )
    print(f"balance = {balance}")
    if balance.get("detail"):
        raise HTTPException(status_code=400, detail=balance["detail"])
    else:
        return balance


@router.get("/get_eth_balance")
async def get_token_balance(data: TokenBalance):
    print("checking eth balance")
    try:
        wallet: dict = await WalletFactory(data.tg_id).get_wallet()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"No Wallets found")
    eth_balance = await GetBalances().get_eth_balance(wallet["wallet_address"])

    if eth_balance.get("detail"):
        raise HTTPException(status_code=400, detail=eth_balance["detail"])
    else:
        return eth_balance
