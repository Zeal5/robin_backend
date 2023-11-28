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


class TokenModel(BaseModel):
    tg_id: int
    token_address: str


class TokenRiskAndSecurityData(BaseModel):
    x: str


@router.get("/get_token_details")
async def get_token_details(data: TokenModel):
    print(data.token_address)
    token_info = await TokenDoc(data.token_address).get_data()

    if token_info.error is None:
        return token_info.model_dump(mode="dict")
    else:
        print(token_info.error)
        HTTPException(status_code=400, detail="Something went wrong")


"""
{
  "code": 1,
  "message": "OK",
  "result": {
    "0xd7e1055aa8ca4bc723788c5e69e38d27b90c5097": {
      "anti_whale_modifiable": "0",
      "buy_tax": "0.05",
      "can_take_back_ownership": "0",
      "cannot_buy": "0",
      "cannot_sell_all": "0",
      "creator_address": "0x1088e4d83f6483530f99807896c909aaf564908c",
      "creator_balance": "0",
      "creator_percent": "0.000000",
      "external_call": "0",
      "hidden_owner": "0",
      "holder_count": "3",
      "holders": [
        {
          "address": "0x663a5c229c09b049e36dcc11a9b0d4a8eb9db214",
          "tag": "UniCrypt",
          "is_contract": 1,
          "balance": "3661.661917763572010459",
          "percent": "0.989999999999999999",
          "is_locked": 1,
          "locked_detail": [
            {
              "amount": "3661.661917763572010459",
              "end_time": "2024-11-01T05:00:00+00:00",
              "opt_time": "2023-11-24T18:19:59+00:00"
            }
          ]
        },
        {
          "address": "0x04bda42de3bc32abb00df46004204424d4cf8287",
          "tag": "",
          "is_contract": 0,
          "balance": "36.986484017813858691",
          "percent": "0.009999999999999999",
          "is_locked": 0
        },
        {
          "address": "0x0000000000000000000000000000000000000000",
          "tag": "Null Address",
          "is_contract": 0,
          "balance": "0.000000000000001",
          "percent": "0.000000000000000000",
          "is_locked": 1
        }
      ],
      "honeypot_with_same_creator": "0",
      "is_anti_whale": "0",
      "is_blacklisted": "0",
      "is_honeypot": "0",
      "is_in_dex": "0",
      "is_mintable": "1",
      "is_open_source": "1",
      "is_proxy": "0",
      "is_whitelisted": "0",
      "owner_address": "0x5c69bee701ef814a2b6a3edd4b1652cb9cc5aa6f",
      "owner_balance": "0",
      "owner_change_balance": "0",
      "owner_percent": "0.000000",
      "personal_slippage_modifiable": "0",
      "selfdestruct": "0",
      "sell_tax": "0.0493",
      "slippage_modifiable": "0",
      "token_name": "Uniswap V2",
      "token_symbol": "UNI-V2",
      "total_supply": "3698.64840178138587015",
      "trading_cooldown": "0",
      "transfer_pausable": "0"
    }
  }
}
"""
