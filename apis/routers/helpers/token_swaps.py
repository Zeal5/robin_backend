import json
from on_chain.buy import Token
from web3 import Web3


# def check_if_address_is_contract_and_checksum(address:str)->bool:
#     web3 = Web3(Web3.HTTPProvider())
#     if not web3.is_address(address):
#         return "invalid address"

#     elif len(web3.eth.get_code(address).hex()) < 3:
#         # print(f"{address} - {len(web3.eth.get_code(address).hex())}")
#         return "address is not a valid contract address"

#     return True


class Swap(Token):
    def __init__(
        self,
        token_address_for_info: str = None,
        buyer_secret: str = None,
        buyer_address: str = None,
        token_to_buy: str = None,
        token_to_sell: str = None,
    ) -> None:

        try:
            super().__init__(
            token_address_for_info,
            buyer_secret,
            buyer_address,
            token_to_buy,
            token_to_sell,
        )
        except Exception as e :
            raise e

    async def buy(self,eth_to_spend:float):
        return await self.swap_eth_for_tokens(eth_to_spend=eth_to_spend)
    
    async def swap_for_eth(self,token_amount_to_sell:float):
        return await self.swap_tokens_for_eth(token_to_spend=token_amount_to_sell)

    async def get_coin_balance(self,_token_address : str):
        return self._get_token_balance(_token_address)