from on_chain.buy import Token
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
# from .helpers.formate_balance import format_number
# from .helpers.wallet_factory import WalletFactory
# from .helpers.token_swaps import Swap
# from .helpers.etherscan_functions import GetBalances
from .fetch_token_details import TokenDoc
from pprint import pprint 

router = APIRouter()


class TokenBalance(BaseModel):
    tg_id: int
    token_address: str 


@router.get("/get_token_details")
async def get_token_details():
    x =  await TokenDoc("0xd9690431807a185a3293F182Bddd123298a0f25a").get_data()
    pprint(x)
    return x



