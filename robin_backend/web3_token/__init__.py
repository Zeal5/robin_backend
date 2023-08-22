from web3 import Web3
import os 
import json
from dotenv import load_dotenv
load_dotenv()

# INFURAT_TOKEN = os.getenv("INFURA_KEYS")
# web3_provider_url = f"https://mainnet.infura.io/v3/{INFURAT_TOKEN}"

web3_provider_url = "http://127.0.0.1:8545"


web3 = Web3(Web3.HTTPProvider(web3_provider_url))
root_dir = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(root_dir,"ERC20.json"), "r") as f:
    token_abi = json.load(f)["abi"]

with open(os.path.join(root_dir,"IUniswapV2Factory.json"), "r") as f:
    factory_abi = json.load(f)["abi"]

with open(os.path.join(root_dir,"IUniswapV2Router02.json"), "r") as f:
    router_abi = json.load(f)["abi"]


