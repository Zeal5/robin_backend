from web3 import Web3
import os 
import json
from dotenv import load_dotenv
load_dotenv()

INFURAT_TOKEN = os.getenv("INFURA_KEYS")
web3_provider_url = f"https://mainnet.infura.io/v3/{INFURAT_TOKEN}"



web3 = Web3(Web3.HTTPProvider(web3_provider_url))

with open("web3_token/ERC20.json") as f:
    token_abi = json.load(f)["abi"]