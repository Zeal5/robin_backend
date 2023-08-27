import asyncio
from web3 import Web3
from . import token_abi, uniswap_router_abi
import time

import json


class Token:
    """Buy token after analyzing metrics (decimals, eth_balance, check_sum)"""
    web3_provider_url = "http://127.0.0.1:8545"

    def __init__(self, token_address:str = None, buyer_secret:str=None, buyer_address:str=None) -> None:
        self.web3 = Web3(Web3.HTTPProvider(Token.web3_provider_url))
        print(f"is connected : {self.web3.is_connected()}")
        self.buyer_address = buyer_address
        self.token_address = token_address
        self.buyer_secret = buyer_secret

        if self.buyer_address is not None and not self.web3.is_checksum_address(self.buyer_address):
            self.buyer_address = self.web3.to_checksum_address(self.buyer_address)

        if self.token_address is not None and not self.web3.is_checksum_address(self.token_address):
            self.token_address = self.web3.to_checksum_address(self.token_address)

        #@TODO this is set to default account for testing only
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
        eth_balance = self.web3.eth.get_balance(self.buyer_address)
        return self.web3.from_wei(eth_balance, 'ether')
    
    async def swap_tokens_for_eth(self,token_amount_to_spend:int):
        amount = await self._get_eth_balance() 
        if amount >= 0:
            print(f"amount {amount}")
            nonce = self.web3.eth.get_transaction_count(self.buyer_address)
            contract = self.web3.eth.contract("0x50A7707F926F99E3640683518870c5F6A6798c11",abi=uniswap_router_abi)
            weth = contract.functions.WETH().call()
            money = token_amount_to_spend *10**18
            print(money)
            print(self.token_address)
            amount_out = contract.functions.getAmountsOut(int(money),[weth,self.token_address]).call()
            print( amount_out[-1] / 10**18)
            return amount_out[-1] / 10**18

