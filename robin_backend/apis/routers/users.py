from database.wallet_manager import (
    check_wallet_exists_for_user,
    _check_user_exists,
    add_keys_when_user,
    add_user_and_keys,
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

    wallet_gen = Wallet().create_wallet(data.secret)
    if wallet_gen:
        if isinstance(data.secret, str):  # create new wallet | old user
            wallet_exists = await check_wallet_exists_for_user(data.tg_id, data.secret)

            if wallet_exists["user"] and wallet_exists["wallet"]:
                return {"message": "wallet already exists"}
            elif wallet_exists["user"]:
                added_keys = await add_keys_when_user(
                    data.tg_id, wallet_gen["secret"], wallet_gen["address"]
                )
                return added_keys, "keys added for existing user"
            else:
                _add_user_and_keys = await add_user_and_keys(
                    data.tg_id, wallet_gen["secret"], wallet_gen["address"]
                )
                return _add_user_and_keys, "keys and user added"

        user_exists = await _check_user_exists(data.tg_id)

        if isinstance(user_exists, int):
            adding_user = await add_keys_when_user(
                tg_id=data.tg_id,
                secret=wallet_gen["secret"],
                address=wallet_gen["address"],
            )
            return adding_user, "adding keys for existing user"

        _add_user_and_keys = await add_user_and_keys(
            data.tg_id, wallet_gen["secret"], wallet_gen["address"]
        )
        return _add_user_and_keys, "keys and user added"

    return "Invalid key"
