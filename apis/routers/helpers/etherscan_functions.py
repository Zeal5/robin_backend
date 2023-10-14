import json
from . import token_abi
from web3 import Web3
from typing import Union, Dict, Awaitable

with open("config.json", "r") as config_file:
    configs = json.load(config_file)


class GetBalances:
    def __init__(self) -> None:
        self.web3 =  Web3(Web3.HTTPProvider(configs["web3_provider_url"]))
        # self.web3 = Web3(Web3.HTTPProvider(configs["blutgang_load_balancer_url"]))

    async def check_eth_balance(self, address: str) -> float:
        return self.web3.eth.get_balance(address)

    async def get_token_balance(
        self, token_address: str, user_address: str
    ) -> Awaitable[Dict[str, Union[str, float]]]:
        """Takes in ERC20 token address(must be already deployed on chain) \n
        and user wallet address and returns the balances held by an account \n
        params:
            `token_address:` ERC20 address
        params:
            `user_address:`  wallet address"""
        try:
            contract = self.web3.eth.contract(address=token_address, abi=token_abi)
            decimals = contract.functions.decimals().call()
            token_balance = contract.functions.balanceOf(user_address).call()
            print(f"contract => {contract}")
            print(f"decimals => {decimals}")
            print(f"balanceOf => {token_balance}")
            token_symbol = contract.functions.symbol().call()
            print(token_symbol)
        except Exception as e:
            print(str(e))
            return {
                "detail": "Invalid contract address.Please check contract address and make sure it an ERC20 address"
            }

        token_balance = token_balance / 10**decimals
        print(token_balance)
        return {"balance": float(token_balance), "symbol": token_symbol}

    async def get_eth_balance(self, user_address: str) -> float:
        try:
            eth_balance = self.web3.eth.get_balance(user_address)
            return {
                "balance": round(float(eth_balance / 10**18),4),
                "symbol": "ETH",
            }  # @TODO use number formater to display amounts better

        except Exception as e:
            print(str(e))
            return {
                "detail": "Invalid contract address.Please check contract address and make sure it an ERC20 address"
            }
