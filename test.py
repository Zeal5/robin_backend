import time
import asyncio

from databse.wallet_manager import add_user_keys




users = [i for i in range(110,112)]


wallets = [f'wallet-{i}' for i in range(10)]


async def test(user):
    tasks = [add_user_keys(user, wallet) for wallet in wallets]
    results = await asyncio.gather(*tasks)
    for idx, wallet in enumerate(wallets):
        print(f"{user} : {wallet} => {results[idx]}")

async def main():
    start_time = time.time()

    # Run the test function concurrently for each user
    tasks = [test(user) for user in users]
    await asyncio.gather(*tasks)

    # End measuring time
    end_time = time.time()

    # Calculate elapsed time
    elapsed_time = end_time - start_time
    print(f"Total time taken: {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(main())
