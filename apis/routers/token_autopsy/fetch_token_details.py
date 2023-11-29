from pprint import pprint
from goplus.token import Token
from web3 import AsyncWeb3, AsyncHTTPProvider
from fastapi import HTTPException
from pydantic import BaseModel
import asyncio
# from . import token_abi as ERC20_token_abi, uniswap_router_abi
from web3.exceptions import ContractLogicError
import json
from . import ERC20_token_abi, ERC165_token_abi
import aiohttp
from typing import Any, Optional, Union, List, Dict
from dataclasses import dataclass
from .token_model_class import TokenInfo, TokenModel, LiquidityModel, PriceChangeModel, TxnsModel, VolumeModel, DexScreenerModel

with open("config.json") as f:
    config = json.load(f)

rpc_url = "blutgang_load_balancer_url"




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
        dex_screener_data = await self.get_dexscreener_data()
        return dex_screener_data


    async def get_dexscreener_data(self):
        async with aiohttp.ClientSession() as Session:
            async with Session.get(f"{config['dexscreener']['base_url']}{config['dexscreener']['search']}{self.token_address}") as response:
                print(response.status)
                if response.status == 200:
                    pairs = await response.json() 
                    print(f"pairs => {pairs}")
                    pair_with_more_liq = None
                    # loop over all pairs and only select pairs which are on eth uniswap v2/v2
                    for pair in pairs['pairs']:
                        if pair.get('chainId') == 'ethereum' and pair.get('dexId') == 'uniswap' and  pair.get('labels')[0] in ['v2','v3']:
                            if pair_with_more_liq is None:
                                pair_with_more_liq = pair

                            elif pair.get('fdv') > pair_with_more_liq.get('fdv'):
                                pair_with_more_liq = pair
                    if pair_with_more_liq is None:
                        raise HTTPException(status_code= 400, detail= "Pair not found on Uniswap ethereum")
                    dexscreener_data = DexScreenerModel.model_validate(pair_with_more_liq)
                    goplus_data = await self.get_goplus_data(dexscreener_data.baseToken.address)
                    return goplus_data, dexscreener_data
                    

                    
                            
                            



    async def get_goplus_data(self,_token_address) -> TokenInfo:
        # Fetch token security details from GoPlus
        data = (
            Token(access_token=None)
            .token_security(
                chain_id="1", addresses=[_token_address]
            )
            .to_dict()
        )
        print(self.token_address,data)
        if data["code"] == 1:
            result_dict = data["result"]
            internal_dict_key = list(result_dict.keys())[0]
            print(internal_dict_key)
            clean_data = result_dict[internal_dict_key]
            # @TODO use TokenInfo.model_validate to validate data 
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
