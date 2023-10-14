import os, json

root_dir = root_dir = os.getcwd()

with open(os.path.join(root_dir, "abis", "ERC20.json"), "r") as f:
    token_abi = json.load(f)["abi"]

with open(os.path.join(root_dir, "abis", "IUniswapV2Factory.json"), "r") as f:
    factory_abi = json.load(f)["abi"]

with open(os.path.join(root_dir, "abis", "IUniswapV2Router02.json"), "r") as f:
    uniswap_router_abi = json.load(f)["abi"]
