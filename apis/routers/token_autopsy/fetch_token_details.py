from pprint import pprint
from goplus.token import Token
from web3 import AsyncWeb3, AsyncHTTPProvider
from fastapi import HTTPException
from pydantic import BaseModel

# from . import token_abi as ERC20_token_abi, uniswap_router_abi
from web3.exceptions import ContractLogicError
import json
from . import ERC20_token_abi, ERC165_token_abi
import aiohttp
from typing import Any, Optional, Union, List, Dict
from dataclasses import dataclass


with open("config.json") as f:
    config = json.load(f)

rpc_url = "blutgang_load_balancer_url"


class TokenInfo(BaseModel):
    anti_whale_modifiable: Optional[str]
    buy_tax: Optional[str]
    can_take_back_ownership: Optional[str]
    cannot_buy: Optional[str]
    cannot_sell_all: Optional[str]
    creator_address: Optional[str]
    creator_balance: Optional[str]
    creator_percent: Optional[str]
    dex: Optional[List[Dict]]
    external_call: Optional[str]
    hidden_owner: Optional[str]
    holder_count: Optional[str]
    holders: Optional[List[Dict]]
    honeypot_with_same_creator: Optional[str]
    is_airdrop_scam: Optional[str]
    is_anti_whale: Optional[str]
    is_blacklisted: Optional[str]
    is_honeypot: Optional[str]
    is_in_dex: Optional[str]
    is_mintable: Optional[str]
    is_open_source: Optional[str]
    is_proxy: Optional[str]
    is_true_token: Optional[str]
    is_whitelisted: Optional[str]
    lp_holder_count: Optional[str]
    lp_holders: Optional[List[Dict]]
    lp_total_supply: Optional[str]
    note: Optional[str]
    other_potential_risks: Optional[str]
    owner_address: Optional[str]
    owner_balance: Optional[str]
    owner_change_balance: Optional[str]
    owner_percent: Optional[str]
    personal_slippage_modifiable: Optional[str]
    selfdestruct: Optional[str]
    sell_tax: Optional[str]
    slippage_modifiable: Optional[str]
    token_name: Optional[str]
    token_symbol: Optional[str]
    total_supply: Optional[str]
    trading_cooldown: Optional[str]
    transfer_pausable: Optional[str]
    trust_list: Optional[str]
    error: Optional[str] = None


class TokenDoc:
    def __init__(self, token_address: str, wallet_address: Optional[str] = None):
        self.web3 = AsyncWeb3(AsyncHTTPProvider(config[rpc_url]))
        self.wallet_address = wallet_address
        self.token_address = token_address
        print(f"new token enterd was {self.token_address}")
        if not self._is_checksum():
            try:
                self.token_address = self.web3.to_checksum_address(token_address)
            except Exception as e:
                print(str(e))
                raise HTTPException(status_code=400, detail="Invalid address enterd")

    def _is_checksum(self) -> bool:
        return self.web3.is_checksum_address(self.token_address)

    async def is_contract(self) -> bool:
        """check if address is contract address or a wallet address \n
        `return` : `bool`"""
        iscontract = await self.web3.eth.get_code(self.token_address)
        return len(iscontract.hex()) > 2

    async def get_data(self):
        data = (
            Token(access_token=None)
            .token_security(
                chain_id="1", addresses=[self.token_address]
            )
            .to_dict()
        )
        print(self.token_address,data)
        if data["code"] == 1:
            result_dict = data["result"]
            internal_dict_key = list(result_dict.keys())[0]
            print(internal_dict_key)
            clean_data = result_dict[internal_dict_key]
            token_info = TokenInfo(**clean_data)
            print("succes getting token security into")
            return token_info
        else:
            print(data)
            print("something went wrong")
            return TokenInfo(error="something went wrong")


"""
        match data:
            case {
                "code": _code,
                "message": _message,
                "result": {
                    self.token_address: {
                        "anti_whale_modifiable": _anti_whale,
                        "buy_tax": _buy_tax,
                        "can_take_back_ownership": _can_take_back_ownership,
                        "cannot_buy": _cannot_buy,
                        "cannot_sell_all": _cannot_sell,
                        "creator_address": _creator_address,
                        "creator_balance": _creator_balance,
                        "creator_percent": _creator_balance_percentage,
                        "external_call": _external_call,
                        "hidden_owner": _hidden_owner,
                        "holder_count": _holder_count,
                        "holders": _X,
                        "honeypot_with_same_creator": _honeypot_with_same_creator,
                        "is_anti_whale": _is_anti_whale,
                        "is_blacklisted": _is_blacklisted,
                        "is_honeypot": _is_honeypot,
                        "is_in_dex": _is_in_dex,
                        "is_mintable": _is_mintable,
                        "is_open_source": _is_open_source,
                        "is_proxy": _is_proxy,
                        "is_whitelisted": _is_whitelisted,
                        "owner_address": _owner_address,
                        "owner_balance": _owner_balance,
                        "owner_change_balance": _owner_change_balance,
                        "owner_percent": _owner_percent,
                        "personal_slippage_modifiable": _personal_slippage_modifiable,
                        "selfdestruct": _self_destruct,
                        "sell_tax": _sell_tax,
                        "slippage_modifiable": _slippage_modifiable,
                        "token_name": _token_name,
                        "token_symbol": _token_symbol,
                        "total_supply": _total_supply,
                        "trading_cooldown": _trading_cooldown,
                        "transfer_pausable": _transfer_pausable,
                    }
                },
            }:
                # Create instances of TokenInfo and TokenResult
                token_info_instance = TokenInfo(_code, _message)
                token_result_instance = TokenResult(
                    _anti_whale,
                    _buy_tax,
                    _can_take_back_ownership,
                    _cannot_buy,
                    _cannot_sell,
                    _creator_address,
                    _creator_balance,
                    _creator_balance_percentage,
                    _external_call,
                    _hidden_owner,
                    _holder_count,
                    _X,
                    _honeypot_with_same_creator,
                    _is_anti_whale,
                    _is_blacklisted,
                    _is_honeypot,
                    _is_in_dex,
                    _is_mintable,
                    _is_open_source,
                    _is_proxy,
                    _is_whitelisted,
                    _owner_address,
                    _owner_balance,
                    _owner_change_balance,
                    _owner_percent,
                    _personal_slippage_modifiable,
                    _self_destruct,
                    _sell_tax,
                    _slippage_modifiable,
                    _token_name,
                    _token_symbol,
                    _total_supply,
                    _trading_cooldown,
                    _transfer_pausable,
                )
                return token_info_instance, token_result_instance

            case _:
                print(data)
                return "Nothiing matched"
"""
