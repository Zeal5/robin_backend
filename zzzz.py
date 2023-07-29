"""


from web3_token import web3
import asyncio
from web3_token.buy import Buy_Token
import time


s = time.time()

tokens = ["0x571E21a545842C6CE596663cdA5CaA8196AC1c7A"]

owner = ["0x755fBECD5FCEf89a27c995E55bF99d1eC1d0e1Fc"]
tasks = []

async def main():
    for i in range(len(tokens)):
        buyer = Buy_Token(tokens[i],owner[i])
        tasks.append(buyer.get_token_balance())

    results = await asyncio.gather(*tasks)
    
    for balance in results:
        print(balance)


asyncio.run(main())

print(time.time() - s)
"""