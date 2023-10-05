from eth_account import Account


class Wallet:
    """Generate a wallet address based on menmonic,private_key
    OR Create new wallet private_key and address if no parameter is given"""

    def __init__(self):
        pass

    def create_wallet(self, private_key: str = None) -> dict | bool:
        account = False
        if private_key is None:
            account = Account.create()
        elif " " in private_key:
            # ("memonic")
            Account.enable_unaudited_hdwallet_features()
            try:
                account = Account.from_mnemonic(private_key, f"m/44'/60'/0'/0")
            except Exception as e:
                raise e
        elif private_key.startswith("0x"):
            # ("0xkey")
            private_key = private_key[2:]
            try:
                account = Account.from_key(private_key)
            except Exception as e:
                raise e
        elif len(private_key) == 64:
            # ("64 len")
            account = Account.from_key(private_key)

        if not account:
            return False
        
        # for a in account:
        print(f"acccccount    =  ==> {account.__doc__}")

        return {
            "address": account.address or "",
            "secret": account._private_key.hex() or "",
        }


# try:
#     w = Wallet()
#     return(w.account)
#     return(w.private_key)
#     return(w.address)
# except Exception as e:
#     return(e)
