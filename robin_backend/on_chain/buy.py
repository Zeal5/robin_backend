import asyncio
from web3 import Web3
from . import token_abi as ERC20_token_abi, uniswap_router_abi
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
        token_address_for_info: str = None,
        buyer_secret: str = None,
        buyer_address: str = None,
        token_to_buy: str = None,
        token_to_sell: str = None,
    ) -> None:
        self.web3 = Web3(Web3.HTTPProvider(Token.web3_provider_url))
        # print(f"is connected : {self.web3.is_connected()}")
        self.buyer_address = buyer_address
        self.token_address_for_info = token_address_for_info
        self.buyer_secret = buyer_secret
        self.token_to_buy = token_to_buy
        self.token_to_sell = token_to_sell

        if buyer_address is not None and not self.web3.is_checksum_address(
            buyer_address
        ):
            self.buyer_address = self.web3.to_checksum_address(buyer_address)

        if token_address_for_info is not None and not self.web3.is_checksum_address(
            token_address_for_info
        ):
            self.token_address_for_info = self.web3.to_checksum_address(
                token_address_for_info
            )

        if token_to_buy is not None and not self.web3.is_checksum_address(token_to_buy):
            self.token_to_buy = self.web3.to_checksum_address(token_to_buy)

        if token_to_sell is not None and not self.web3.is_checksum_address(
            token_to_sell
        ):
            self.token_to_sell = self.web3.to_checksum_address(token_to_sell)

        # @TODO this is set to default account for testing only
        self.account = self.web3.eth.default_account = self.buyer_address

    #@TODO update decimals and other info related to token to db(create a class lvl dict to hold that info?) to reduce the calls made to rpc
    async def _get_decimals(self, _token: str = None) -> int:
        """Get decimals of a contract"""

        if _token is None:
            _token = self.token_address_for_info

        print(f"token = {_token}")
        print(f"is check_sum {self.web3.is_checksum_address(_token)}")
        contract = self.web3.eth.contract(
            address=_token, abi=ERC20_token_abi
        )
        decimals = contract.functions.decimals().call()
        print(f"decimals {decimals}")

        return decimals

    async def get_token_balance(self, _token: str = None) -> int | float:
        """Return token balance after dividing by token decimals"""
        if _token is None:
            _token = self.token_address_for_info

        contract = self.web3.eth.contract(address=_token, abi=ERC20_token_abi)
        token_balance = contract.functions.balanceOf(self.buyer_address).call()

        decimals = await self._get_decimals(_token=_token)
        token_balance = token_balance / 10**decimals

        return token_balance

    async def _get_eth_balance(self) -> int:
        eth_balance = self.web3.eth.get_balance(self.buyer_address)
        return self.web3.from_wei(eth_balance, "ether")

    # @TODO only approves tokens for router and use _get_decimal automatically
    async def _approve_tokens(
        self, amount_to_approve: int, _token_to_approve: str = None
    ):
        if _token_to_approve is None:
            _token_to_approve = self.token_address_for_info

        token_contract = self.web3.eth.contract(_token_to_approve, abi=ERC20_token_abi)
        print("token_contract created succesfully")
        approve_txn = token_contract.functions.approve(
            router_address,
            amount_to_approve
            * 10 ** (await self._get_decimals(_token=_token_to_approve)),
        ).build_transaction(
            {
                "from": self.buyer_address,
                "gasPrice": self.web3.eth.gas_price,
                "nonce": self.web3.eth.get_transaction_count(self.buyer_address),
            }
        )
        print(approve_txn)
        signed_approve_txn = self.web3.eth.account.sign_transaction(
            approve_txn, private_key=self.buyer_secret
        )

        self.web3.eth.send_raw_transaction(signed_approve_txn.rawTransaction)
        return approve_txn

    async def swap_tokens_for_tokens(self, token_amount_to_spend: int):
        # @TODO get token decimals using _get_decimals method
        if 3 > 0:
            await self._approve_tokens(
                amount_to_approve=token_amount_to_spend,_token_to_approve = self.token_to_sell
            )

            path = [self.token_to_sell, self.token_to_buy]
            nonce = self.web3.eth.get_transaction_count(self.buyer_address)
            contract = self.web3.eth.contract(router_address, abi=uniswap_router_abi)
            money = token_amount_to_spend * 10** (await self._get_decimals(_token = self.token_to_sell))
            print(f"path {path}")
            amount_out = contract.functions.getAmountsOut(
                int(money), path
            ).call()
            print(amount_out)
            print(f"amount out dai -> usdt {amount_out[0] / (10**(await self._get_decimals(_token = path[0])))} - {amount_out[1] / (10**(await self._get_decimals(_token = path[1])))}")
            print('args')
            # @TODO set custom slipage
            buy_token = contract.functions.swapExactTokensForTokens(
                token_amount_to_spend * 10**(await self._get_decimals(_token = self.token_to_sell)),
                int(96 *10**(await self._get_decimals(_token = self.token_to_buy))),
                path,
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
