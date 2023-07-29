import asyncio
from . import web3, token_abi
import json


class Buy_Token:
    """Buy token afater analyzing metrics (decimals, eth_balance, check_sum)"""

    def __init__(self, token_address, buyer_address) -> None:
        self.buyer_address = buyer_address
        self.token = token_address

        if not web3.is_checksum_address(self.buyer_address):
            self.buyer_address = web3.to_checksum_address(self.buyer_address)

        if not web3.is_checksum_address(self.token):
            self.token = web3.to_checksum_address(self.token)
        self.account = web3.eth.default_account = self.buyer_address

    async def get_token_balance(self) -> int:
        loop = asyncio.get_event_loop()

        contract = web3.eth.contract(address=self.token, abi=token_abi)
        token_balance = await loop.run_in_executor(None,lambda :contract.functions.balanceOf(self.buyer_address).call())
        decimals = await self.get_decimals()
        token_balance = token_balance / (10**decimals)

        return token_balance

    async def get_decimals(self) -> int:
        loop = asyncio.get_event_loop()
        contract = web3.eth.contract(address=self.token, abi=token_abi)
        decimals = await loop.run_in_executor(None,lambda : contract.functions.decimals().call())
        return decimals
