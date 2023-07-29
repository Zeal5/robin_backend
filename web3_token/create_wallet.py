from eth_account import Account


class Wallet:
    """Generate a wallet address based on menmonic,private_key
    OR Create new wallet private_key and address if no parameter is given"""

    def __init__(self, private_key: str = None):
        if " " in private_key:
            print("memonic")
            Account.enable_unaudited_hdwallet_features()
            self.account = Account.from_mnemonic(private_key, f"m/44'/60'/0'/0")
        elif private_key.startswith("0x"):
            print("0xkey")
            private_key = private_key[2:]
            self.account = Account.from_key(private_key)
        elif len(private_key) == 64:
            print("64 len")

            self.account = Account.from_key(private_key)

        else:
            print("none")
            self.account = Account.create()

        self.address = self.account.address
        self.private_key = self.account._private_key.hex()


try:
    w = Wallet()
    print(w.account)
    print(w.private_key)
    print(w.address)
except Exception as e:
    print(e)
