from database.wallet_manager import add_user_keys, check_user_exists
from web3_token.create_wallet import Wallet
from fastapi import APIRouter
from typing import Optional, Union

from pydantic import BaseModel

router = APIRouter()

class User_Wallet(BaseModel):
    id: int
    secret: Optional[str] 


# This function is called to add users and keys to the database
@router.post("/user")
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
    print('start')
    if await check_user_exists(data.id): #when want to generate new wallet keys and user is already present in db 
        print('step2')
        wallet1 = Wallet().create_wallet(data.secret)
        print(wallet1)
        return wallet1['address']

    # new_id = await add_user_keys(tg_id)
    # if isinstance(secret, str) and secret.lower() == "true":
    #     print(secret)
    #     print(type(secret))
    #     return "True"

    # print(secret)
    # print(type(secret))
