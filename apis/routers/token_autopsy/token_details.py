from on_chain.buy import Token
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
# from .helpers.formate_balance import format_number
# from .helpers.wallet_factory import WalletFactory
# from .helpers.token_swaps import Swap
# from .helpers.etherscan_functions import GetBalances
from .fetch_token_details import TokenDoc

router = APIRouter()


class TokenModel(BaseModel):
    tg_id: int
    token_address: str


@router.get("/get_token_details")
async def get_token_details(data: TokenModel):
    print(data.token_address)
    token_security_data, dexscreener_data = await TokenDoc(
        data.token_address
    ).get_data()

    return {
        "token_security_data": token_security_data,
        "dexscreener_data": dexscreener_data,
    }

