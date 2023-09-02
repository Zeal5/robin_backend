import asyncio
from web3 import Web3
from . import token_abi as ERC20_token_abi, uniswap_router_abi
from web3.exceptions import ContractLogicError
import time

import json

with open("config.json") as f:
    config = json.load(f)

# @TODO add router address in config

router_address = "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D"
weth_address = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
dai_address = "0x6B175474E89094C44Da98b954EedeAC495271d0F"


class Token:
    """Buy token after analyzing metrics (decimals, eth_balance, check_sum)"""

    def __init__(
        self,
        token_address_for_info: str = None,
        buyer_secret: str = None,
        buyer_address: str = None,
        token_to_buy: str = None,
        token_to_sell: str = None,
    ) -> None:
        self.web3 = Web3(Web3.HTTPProvider(config["web3_provider_url"]))
        # print(f"is connected : {self.web3.is_connected()}")
        self.buyer_address = buyer_address
        self.token_address_for_info = token_address_for_info
        self.buyer_secret = buyer_secret
        self.token_to_buy = token_to_buy
        self.token_to_sell = token_to_sell
        self.has_faulty_address = False

        if buyer_address is not None and not self.web3.is_checksum_address(
            buyer_address
        ):
            self.buyer_address =  self._convert_to_checksum(buyer_address)

        if token_address_for_info is not None and not self.web3.is_checksum_address(
            token_address_for_info
        ):
            self.token_address_for_info = self._convert_to_checksum(
                token_address_for_info
            )

        if token_to_buy is not None and not self.web3.is_checksum_address(token_to_buy):
            self.token_to_buy = self._convert_to_checksum(token_to_buy)

        if token_to_sell is not None and not self.web3.is_checksum_address(
            token_to_sell
        ):
            self.token_to_sell = self._convert_to_checksum(token_to_sell)

        # @TODO this is set to default account for testing only
        self.account = self.web3.eth.default_account = self.buyer_address
       

    def _convert_to_checksum(self, _address: str):
        try:
            self.web3.to_checksum_address(_address)
        except Exception as e:
            self.has_faulty_address = True
            raise e

    # @TODO update decimals and other info related to token to db(create a class lvl dict to hold that info?) to reduce the calls made to rpc
    async def _get_decimals(self, _token: str = None) -> int:
        """Get decimals of a contract"""

        if _token is None:
            _token = self.token_address_for_info

        contract = self.web3.eth.contract(address=_token, abi=ERC20_token_abi)
        decimals = contract.functions.decimals().call()
        print(f"token = {_token} decimals {decimals}")

        return decimals

    async def _get_token_balance(self, _token: str = None) -> int | float:
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

    async def _check_allowance(self, _token: str = None) -> float:
        if _token is None:
            _token = self.token_address_for_info

        contract = self.web3.eth.contract(_token, abi=ERC20_token_abi)
        allowance = contract.functions.allowance(
            router_address, self.buyer_address
        ).call()
        print(f"allowance = {allowance}")
        return allowance / 10 ** await self._get_decimals(_token)

    # @TODO only approves tokens for router and use _get_decimal automatically
    async def _approve_tokens(
        self, amount_to_approve: int, _token_to_approve: str = None
    ):
        if _token_to_approve is None:
            _token_to_approve = self.token_address_for_info

        allowance = await self._check_allowance(_token_to_approve)
        if allowance >= amount_to_approve:
            return True

        token_contract = self.web3.eth.contract(_token_to_approve, abi=ERC20_token_abi)
        try:
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
        except ContractLogicError as e:
            raise e

        print(approve_txn)
        signed_approve_txn = self.web3.eth.account.sign_transaction(
            approve_txn, private_key=self.buyer_secret
        )

        self.web3.eth.send_raw_transaction(signed_approve_txn.rawTransaction)
        return approve_txn

    async def _get_router_contract(self):
        contract = self.web3.eth.contract(router_address, abi=uniswap_router_abi)
        return contract

    async def _get_amounts_out(
        self,
        amount_in: int,
        token_in_address: str = None,
        token_out_address: str = None,
    ) -> list:
        if token_out_address is None:
            token_out_address = weth_address
        if token_in_address is None:
            token_in_address = weth_address

        path = [token_in_address, token_out_address]
        if token_out_address == token_in_address:
            return [1 * 10**18, 1 * 10**18], path
        contract = await self._get_router_contract()
        amounts_out = contract.functions.getAmountsOut(int(amount_in), path).call()
        print(amounts_out)
        print(
            f"amount out {token_in_address} -> {token_out_address}\n{amounts_out[0] / (10**(await self._get_decimals(_token = path[0])))} - {amounts_out[1] / (10**(await self._get_decimals(_token = path[1])))}"
        )
        return amounts_out, path

    async def swap_tokens_for_tokens(self, token_amount_to_spend: int):
        # @TODO get token decimals using _get_decimals method also correct if statment
        token_balance = await self._get_token_balance(_token=self.token_to_sell)
        if token_balance <= token_amount_to_spend:
            await self._approve_tokens(
                amount_to_approve=token_amount_to_spend,
                _token_to_approve=self.token_to_sell,
            )

            path = [self.token_to_sell, self.token_to_buy]
            contract = (
                await self._get_router_contract
            )  # self.web3.eth.contract(router_address, abi=uniswap_router_abi)
            money = token_amount_to_spend * 10 ** (
                await self._get_decimals(_token=self.token_to_sell)
            )
            print(f"path {path}")
            amount_out = await self._get_amounts_out(money, *path)

            print("args")
            # @TODO set custom slipage
            try:
                buy_token = contract.functions.swapExactTokensForTokens(
                    token_amount_to_spend
                    * 10 ** (await self._get_decimals(_token=self.token_to_sell)),
                    # amount out expected slippage
                    int(
                        90 * 10 ** (await self._get_decimals(_token=self.token_to_buy))
                    ),
                    path,
                    self.buyer_address,
                    int(time.time() + 1000),
                ).build_transaction(
                    {
                        "from": self.buyer_address,
                        "gasPrice": self.web3.eth.gas_price,
                        "nonce": self.web3.eth.get_transaction_count(
                            self.buyer_address
                        ),
                    }
                )
            except ContractLogicError as e:
                raise e

            signed_approve_txn = self.web3.eth.account.sign_transaction(
                buy_token, private_key=self.buyer_secret
            )
            tx_Hash = self.web3.eth.send_raw_transaction(
                signed_approve_txn.rawTransaction
            )
            tx = self.web3.eth.get_transaction(tx_Hash)

            print(f"tx => {tx}")

            return {
                "hash": tx_Hash.hex(),
                "nonce": tx["nonce"],
                "from": tx["from"],
                "to": tx["to"],
            }
        else:
            return {
                "error": f"token amount({token_balance}) is less then amount specified({token_amount_to_spend})"
            }

    async def swap_eth_for_tokens(self, eth_to_spend: int):
        eth_balance = await self._get_eth_balance()
        print(self.buyer_address)
        if  eth_balance >= eth_to_spend:
            print(f"ethbalance = {eth_balance}")
            contract = await self._get_router_contract()
            amounts_out, path = await self._get_amounts_out(
                eth_to_spend * 10**18, token_out_address=dai_address
            )
            try:
                buy_token = contract.functions.swapExactETHForTokens(
                    0, path, self.buyer_address, int(time.time() + 100)
                ).build_transaction(
                    {
                        "from": self.buyer_address,
                        "value": amounts_out[0],
                        "gasPrice": self.web3.eth.gas_price,
                        "nonce": self.web3.eth.get_transaction_count(
                            self.buyer_address
                        ),
                    }
                )
            except ContractLogicError as e:
                raise e

            signed_approve_txn = self.web3.eth.account.sign_transaction(
                buy_token, private_key=self.buyer_secret
            )
            tx_Hash = self.web3.eth.send_raw_transaction(
                signed_approve_txn.rawTransaction
            )
            tx = self.web3.eth.get_transaction(tx_Hash)

            print(f"tx => {tx}")

            return {
                "hash": tx_Hash.hex(),
                "nonce": tx["nonce"],
                "from": tx["from"],
                "to": tx["to"],
            }
        else:
            return {
                "error": f"eth balance ({eth_balance}) is less then {eth_to_spend} "
            }

    async def swap_tokens_for_eth(self, token_to_spend: str):
        token_to_spend = token_to_spend * 10 ** await self._get_decimals(
            self.token_to_sell
        )
        token_balance = await self._get_token_balance(_token=dai_address)
        if token_balance < token_to_spend:
            print(
                f"token balance = {token_balance *10** await self._get_decimals(self.token_to_sell)}"
            )
            await self._approve_tokens(token_to_spend, dai_address)
            contract = await self._get_router_contract()
            amounts_out, path = await self._get_amounts_out(
                token_to_spend,
                token_in_address=self.token_to_sell,
            )
            print(amounts_out, path)
            try:
                buy_token = contract.functions.swapTokensForExactETH(
                    amounts_out[1] - 1 * 10**17,
                    amounts_out[0],
                    path,
                    self.buyer_address,
                    int(time.time() + 10),
                ).build_transaction(
                    {
                        "from": self.buyer_address,
                        "gasPrice": self.web3.eth.gas_price,
                        "nonce": self.web3.eth.get_transaction_count(
                            self.buyer_address
                        ),
                    }
                )
            except ContractLogicError as e:
                raise e

            signed_approve_txn = self.web3.eth.account.sign_transaction(
                buy_token, private_key=self.buyer_secret
            )
            tx_Hash = self.web3.eth.send_raw_transaction(
                signed_approve_txn.rawTransaction
            )
            tx = self.web3.eth.get_transaction(tx_Hash)

            print(f"tx => {tx}")

            return {
                "hash": tx_Hash.hex(),
                "nonce": tx["nonce"],
                "from": tx["from"],
                "to": tx["to"],
            }

        else:
            return {
                "error": f"token balance({token_balance}) is less then amount specifies({token_to_spend})"
            }
