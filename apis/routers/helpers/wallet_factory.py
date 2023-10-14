from database.wallet_manager import get_active_wallet, get_slippage


class WalletFactory:
    """Create a new Wallet factory methods include getting wallet info \n
    this class doesn't retain the instances"""

    def __init__(self, tg_id) -> None:
        self.tg_id: int = tg_id

    async def get_wallet(self) -> dict:
        try:
            wallet = await get_active_wallet(self.tg_id)
            slippage = await get_slippage(wallet.user_id)
            print(f"factory -- {slippage}")

            print(
                f"""
                from  wallet factory 
                "wallet_name": {wallet.name},\n
                "user_id": {wallet.user_id},\n
                "wallet_address": {wallet.address},\n
                "secret": {wallet.secret},\n
                "slippage" : {slippage}
                """
            )
            return {
                "wallet_name": wallet.name,
                "user_id": wallet.user_id,
                "wallet_address": wallet.address,
                "wallet_secret": wallet.secret,
                "slippage": slippage or 7,
            }
        except Exception as e:
            raise e
