import asyncio
from web3 import Web3

async def get_token_balance(web3_provider_url, contract_address, wallet_address):
    # Connect to the Ethereum node
    web3 = Web3(Web3.HTTPProvider(web3_provider_url))

    # Load the token contract ABI
    token_abi = [...]  # Replace this with the ABI of the token contract

    # Create a contract object
    token_contract = web3.eth.contract(address=contract_address, abi=token_abi)

    # Get the balance of the specified wallet address
    try:
        balance = await asyncio.to_thread(token_contract.functions.balanceOf(wallet_address).call)
        return balance
    except Exception as e:
        print(f"Error while fetching balance: {e}")
        return None

# Example usage
async def main():
    web3_provider_url = "https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID"
    contract_address = "0x123...789"  # Replace with the contract address of token X
    wallet_address = "0xabc...def"    # Replace with the wallet address you want to check

    balance = await get_token_balance(web3_provider_url, contract_address, wallet_address)
    if balance is not None:
        print(f"Token X balance for address {wallet_address}: {balance}")

if __name__ == "__main__":
    asyncio.run(main())
