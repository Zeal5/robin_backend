import asyncio
from web3 import Web3
from . import token_abi, uniswap_router_abi
import time

import json

# @TODO add router address in config

router_address = "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D"
weth_address = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
dai_address = "0x6B175474E89094C44Da98b954EedeAC495271d0F"


class Token:
    """Buy token after analyzing metrics (decimals, eth_balance, check_sum)"""

    web3_provider_url = "http://127.0.0.1:8545"

    def __init__(
        self,
        token_address: str = None,
        buyer_secret: str = None,
        buyer_address: str = None,
    ) -> None:
        self.web3 = Web3(Web3.HTTPProvider(Token.web3_provider_url))
        print(f"is connected : {self.web3.is_connected()}")
        self.buyer_address = buyer_address
        self.token_address = token_address
        self.buyer_secret = buyer_secret

        if self.buyer_address is not None and not self.web3.is_checksum_address(
            self.buyer_address
        ):
            self.buyer_address = self.web3.to_checksum_address(self.buyer_address)

        if self.token_address is not None and not self.web3.is_checksum_address(
            self.token_address
        ):
            self.token_address = self.web3.to_checksum_address(self.token_address)

        # @TODO this is set to default account for testing only
        self.account = self.web3.eth.default_account = self.buyer_address

    async def _get_decimals(self) -> int:
        """Get decimals of a contract"""
        loop = asyncio.get_event_loop()
        contract = self.web3.eth.contract(address=self.token_address, abi=token_abi)
        decimals = await loop.run_in_executor(
            None, lambda: contract.functions.decimals().call()
        )
        return decimals

    async def get_token_balance(self) -> int:
        """Return token balance after dividing by token decimals"""
        loop = asyncio.get_event_loop()

        contract = self.web3.eth.contract(address=self.token_address, abi=token_abi)
        token_balance = await loop.run_in_executor(
            None, lambda: contract.functions.balanceOf(self.buyer_address).call()
        )
        decimals = await self._get_decimals()
        token_balance = token_balance / (10**decimals)

        return token_balance

    async def _get_eth_balance(self) -> int:
        eth_balance = self.web3.eth.get_balance(self.buyer_address)
        return self.web3.from_wei(eth_balance, "ether")
    

    #@TODO only approves tokens for router and use _get_decimal automatically
    async def _approve_tokens(self, amount_to_approve):
        token_contract = self.web3.eth.contract(dai_address, abi=token_abi)
        print('token_contract created succesfully')
        approve_txn = token_contract.functions.approve(
            router_address, amount_to_approve *10**18
        ).build_transaction(
            {
                "from": self.buyer_address,
                "gasPrice": self.web3.eth.gas_price,
                "nonce": self.web3.eth.get_transaction_count(self.buyer_address)
            }
        )
        print(approve_txn)
        signed_approve_txn = self.web3.eth.account.sign_transaction(approve_txn, private_key=self.buyer_secret)

        self.web3.eth.send_raw_transaction(signed_approve_txn.rawTransaction)
        return approve_txn

    async def swap_tokens_for_eth(self, token_amount_to_spend: int):
        # @TODO get token decimals using _get_decimals method
        amount = await self._get_eth_balance()
        if amount > 0:
            print(f"amount {amount}")
            await self._approve_tokens(token_amount_to_spend)
            nonce = self.web3.eth.get_transaction_count(self.buyer_address)
            contract = self.web3.eth.contract(router_address, abi=uniswap_router_abi)
            weth = contract.functions.WETH().call()
            money = token_amount_to_spend * 10**18
            print(money)
            print(self.token_address)
            amount_out = contract.functions.getAmountsOut(
                int(money), [dai_address, self.token_address]
            ).call()
            print(f"amount out dai -> weth {amount_out[0] / (10**18)} - {amount_out[1] / (10**18)}")
            print('args')
            print(token_amount_to_spend * 10**18,
                int(0.96 *10**18),
                [dai_address, self.token_address],
                self.buyer_address,
                int(time.time() + 10))

            # @TODO set custom slipage
            buy_token = contract.functions.swapExactTokensForTokens(
                token_amount_to_spend * 10**18,
                int(0.96 *10**18),
                [dai_address, self.token_address],
                self.buyer_address,
                int(time.time() + 1000)
            ).build_transaction(
                {
                    "from": self.buyer_address,
                    "gasPrice": self.web3.eth.gas_price, 
                    "nonce": self.web3.eth.get_transaction_count(self.buyer_address),
                }
            )
            signed_approve_txn = self.web3.eth.account.sign_transaction(buy_token, private_key=self.buyer_secret)

            self.web3.eth.send_raw_transaction(signed_approve_txn.rawTransaction)
            print(signed_approve_txn)
            return  signed_approve_txn
