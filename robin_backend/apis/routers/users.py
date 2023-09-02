from database.wallet_manager import (
    check_wallet_exists_for_user,
    _check_user_exists,
    add_keys_when_user,
    add_user_and_keys,
    get_wallets
)
from on_chain.create_wallet import Wallet
from fastapi import APIRouter
from typing import Optional, Union

from pydantic import BaseModel

router = APIRouter()


class User_Wallet(BaseModel):
    tg_id: int
    secret: Optional[str] = None


# This function is called to add users and keys to the database
@router.post("/create_wallet")
async def add_user_wallet(data: User_Wallet):
    """Adds Users and keys to databse
    when user keys are provided adds wallet to db \n
    if no secret value is passed into query string then new wallet is created
    bcz secret defaults to False

    Args:
        ``tg_id`` : Users tg_id
        ``secret``: Wallet secret key (24|12 letters or hex)
    Returns:
        ``Bool`` : True is key added successfully else false"""
    #pass secret to create wallet from secret else new walelt is created
    wallet_gen = Wallet().create_wallet(data.secret)
    #Generate next wallet name
    try:
        wallets = await get_wallets(data.tg_id)
        last_wallet = wallets[-1]
        wallet_number = last_wallet.name.split()[-1]
        wallet_name = f"Wallet {int(wallet_number) + 1}"
        print(f"last wallet = {last_wallet.name}")
    except Exception as e:
        wallet_name = "Wallet 1"


    if wallet_gen:
        if isinstance(data.secret, str):  # create new wallet | old user
            wallet_and_user_exists = await check_wallet_exists_for_user(data.tg_id, data.secret)

            if wallet_and_user_exists["user"] and wallet_and_user_exists["wallet"]:
                return {"detail": "wallet secret key already in use already exists"}
            elif wallet_and_user_exists["user"]:
                added_keys = await add_keys_when_user(
                    data.tg_id, wallet_gen["secret"], wallet_gen["address"],wallet_name
                )
                if added_keys:
                    return {"wallet_name":wallet_name,**wallet_gen}
            else:
                _add_user_and_keys = await add_user_and_keys(
                    data.tg_id, wallet_gen["secret"], wallet_gen["address"], wallet_name
                )
                if _add_user_and_keys:
                    return {"wallet_name":wallet_name,**wallet_gen}

        try:
            user_exists = await _check_user_exists(data.tg_id)
        except Exception as e:
            user_exists = "none"
        if isinstance(user_exists, int):
            adding_user = await add_keys_when_user(
                tg_id=data.tg_id,
                secret=wallet_gen["secret"],
                address=wallet_gen["address"],
                wallet_name=wallet_name
            )
            if adding_user:
                return {"wallet_name":wallet_name,**wallet_gen}

        _add_user_and_keys = await add_user_and_keys(
            data.tg_id, wallet_gen["secret"], wallet_gen["address"],wallet_name
        )
        if _add_user_and_keys:
            return {"wallet_name":wallet_name,**wallet_gen}

    return {"detail":"Invalid key"}
