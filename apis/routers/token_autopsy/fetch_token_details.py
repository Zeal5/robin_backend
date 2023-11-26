from pprint import pprint 
from goplus.token import Token
from web3 import AsyncWeb3, AsyncHTTPProvider
from fastapi import HTTPException
# from . import token_abi as ERC20_token_abi, uniswap_router_abi
from web3.exceptions import ContractLogicError
import json
from . import ERC20_token_abi, ERC165_token_abi
import aiohttp
from typing import Any,Optional

with open("config.json") as f:
    config = json.load(f)

rpc_url = "blutgang_load_balancer_url"


class TokenDoc:
    def __init__(self, token_address: str, wallet_address: Optional[str] = None):
        self.web3 = AsyncWeb3(AsyncHTTPProvider(config[rpc_url]))
        self.wallet_address = wallet_address
        self.token_address = token_address
        if not self._is_checksum():
            try:
                self.token_address = self.web3.to_checksum_address(token_address)
            except Exception as e:
                print(str(e))
                raise HTTPException(status_code=400, detail="Invalid address enterd")

    def _is_checksum(self) -> bool:
        return self.web3.is_checksum_address(self.token_address)

    async def is_contract(self) -> bool:
        """ check if address is contract address or a wallet address \n
        `return` : `bool` """
        iscontract = await self.web3.eth.get_code(self.token_address)
        return len(iscontract.hex()) > 2 

    async def get_data(self,token_addresses : list[str] = []):
        if not self.is_contract():
            raise HTTPException(status_code=400, detail="Not a contract address")

        token_addresses.append(self.token_address)
        data = Token(access_token= None).token_security(
            chain_id= '1', addresses=token_addresses, **{"_request_timeout":10})
        return data
        # url = "https://api.geckoterminal.com/api/v2"
        # headers = {"accept" : "application/json"}
        # network = 'eth'
        #
        # async with aiohttp.ClientSession() as Session:
        #     async with Session.get(fr"{url}/networks/{network}/tokens/0x6982508145454Ce325dDbE47a25d4ec3d2311933", headers = headers) as response:
        #     # async with Session.get(f"https://api.geckoterminal.com/api/v2/networks/eth/tokens/0x6982508145454Ce325dDbE47a25d4ec3d2311933", headers = headers) as response:
        #         print(response.status)
        #         return await response.json()

