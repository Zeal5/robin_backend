import asyncio
from . import web3, token_abi, uniswap_router_abi

import json


class Token:
    """Buy token after analyzing metrics (decimals, eth_balance, check_sum)"""

    def __init__(self, token_address:str = None, buyer_secret:str=None, buyer_address:str=None) -> None:
        self.web3 = web3
        self.buyer_address = buyer_address
        self.token = token_address
        self.buyer_secret = buyer_secret

        if self.buyer_address != None and not self.web3.is_checksum_address(self.buyer_address):
            self.buyer_address = self.web3.to_checksum_address(self.buyer_address)

        if self.token != None and not self.web3.is_checksum_address(self.token):
            self.token = self.web3.to_checksum_address(self.token)
        self.account = self.web3.eth.default_account = self.buyer_address

    async def _get_decimals(self) -> int:
        """Get decimals of a contract"""
        loop = asyncio.get_event_loop()
        contract = self.web3.eth.contract(address=self.token, abi=token_abi)
        decimals = await loop.run_in_executor(
            None, lambda: contract.functions.decimals().call()
        )
        return decimals
    

    async def get_token_balance(self) -> int:
        """Return token balance after dividing by token decimals """
        loop = asyncio.get_event_loop()

        contract = self.web3.eth.contract(address=self.token, abi=token_abi)
        token_balance = await loop.run_in_executor(
            None, lambda: contract.functions.balanceOf(self.buyer_address).call()
        )
        decimals = await self._get_decimals()
        token_balance = token_balance / (10**decimals)

        return token_balance
    
    async def _get_eth_balance(self) -> int:
        eth_balance = web3.eth.get_balance(self.buyer_address)
        return web3.from_wei(eth_balance, 'ether')
    
    async def swap_tokens_for_tokens(self):
        amount = await self._get_eth_balance() 
        if amount >= 0:
            print(f"amount {amount}")
