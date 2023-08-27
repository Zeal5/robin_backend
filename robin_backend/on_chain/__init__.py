
import os 
import json
from dotenv import load_dotenv
load_dotenv()

# INFURAT_TOKEN = os.getenv("INFURA_KEYS")
# web3_provider_url = f"https://mainnet.infura.io/v3/{INFURAT_TOKEN}"



#The geth_poa_middleware is required by BSC, Polygon and Fantom since they are all Proof-of-Authority chains.
#w3.middleware_onion.inject(geth_poa_middleware, layer=0)

root_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(root_dir,"abis","ERC20.json"), "r") as f:
    token_abi = json.load(f)["abi"]

with open(os.path.join(root_dir,"abis","IUniswapV2Factory.json"), "r") as f:
    factory_abi = json.load(f)["abi"]

with open(os.path.join(root_dir,"abis","IUniswapV2Router02.json"), "r") as f:
    uniswap_router_abi = json.load(f)["abi"]


