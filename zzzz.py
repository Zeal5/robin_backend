import requests
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
import os,time
from web3_token import token_abi,web3_provider_url, factory_abi, router_abi
from web3 import Web3



# w3 = Web3(Web3.HTTPProvider(web3_provider_url))
# print(w3.is_connected())
# block = w3.eth.get_block('latest')

# router = w3.eth.contract(address="0x2D6774d043922Df98B195e7496C2ecc8E1AC2c49",abi=factory_abi)
# print(router.functions.allPairsLength().call())



# def main():
#     urls = "http://127.0.0.1:8000/1234/secret/address"

#     response = requests.get(urls)
#     print(response.text)
#     print(response.status_code)





# if __name__ == "__main__":
#     main()



class Fk:
    def __init__(self):
        self.id = 6
        print(f"User(id={self.id!r})")

a = Fk()

