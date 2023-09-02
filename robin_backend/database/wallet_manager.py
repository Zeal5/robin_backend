from .models import Users, Wallets, ActiveWallets
from . import Session
from sqlalchemy.future import select
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import insert, select, exists
import functools


# test wrapper afterwards
def get_wallets_count(func):
    @functools.wraps(func)
    async def wraped(tg_id, *args, **kwargs):
        wallets = {i.id: i.address for i in await get_wallets(tg_id)}
        print(len(wallets))
        print(wallets)
        if len(wallets.keys()) <= 6:
            print("keys less then 7")
            return await func(tg_id, *args, **kwargs)
        else:
            return "Max 7 wallets are allowed"

    return wraped


async def _check_user_exists(_id: int) -> int | dict:
    """Checks if user with tg_id exists in database

    Args:
        ``tg_id``: The Telegram ID of user

    Returns:
        ``bool`` : True if user with tg_id exists
    """
    async with Session() as s:
        async with s.begin():
            try:
                users = await s.execute(select(Users).filter(Users.tg_id == _id))
                return users.scalar_one().id
            except NoResultFound as e:
                raise e


async def check_wallet_exists_for_user(_id: int, secret: str) -> dict:
    return_dict = {"user": False, "wallet": False}
    user_id: int = await _check_user_exists(_id)
    async with Session() as session:
        async with session.begin():
            try:
                if not isinstance(user_id, dict):
                    return_dict["user"] = True
                    stmt = select(
                        exists()
                        .where(Wallets.user_id == user_id)
                        .where(Wallets.secret == secret)
                    )
                    result = await session.execute(stmt)
                    secret_exists = result.scalar_one()
                    if secret_exists:
                        return_dict["wallet"] = True
                    return return_dict
                else:
                    return return_dict
            except NoResultFound as e:
                return {"error": e}


async def add_user_and_keys(tg_id: int, secret: str, address: str,wallet_name:str) -> bool | dict:
    """Add user, wallets to the database.

    Args:
        ``tg_id`` : The Telegram ID of the user.\n
        ``secret`` : The secret Key for Wallet authentication

    Returns:
        ``Bool``: True if user and wallet was added successfully.
    """

    async with Session() as s:
        async with s.begin():
            try:
                new_user = Users(tg_id=tg_id)
                new_wallet = Wallets(user=new_user, secret=secret, address=address,name=wallet_name)
                s.add(new_user)
                s.add(new_wallet)
                await s.flush()
                print(f"new user = {new_user.id}")
                print(f"new_wallet = {new_wallet.id}")
                Users
                new_active_wallet = ActiveWallets(user_id=new_user.id, wallet_id=new_wallet.id)
                s.add(new_active_wallet)
                await s.commit()
                return True
            except Exception as e:
                raise e


@get_wallets_count
async def add_keys_when_user(tg_id: int, secret: str, address: str, wallet_name:str) -> bool | dict:
    async with Session() as s:
        async with s.begin():
            try:
                existing_user = await s.execute(
                    select(Users).filter(Users.tg_id == tg_id)
                )
                user_id = existing_user.scalars().one().id
                # user = existing_user.scalar_one()
                wallet = Wallets(user_id=user_id, secret=secret, address=address,name = wallet_name)
                s.add(wallet)
                await s.commit()
                return True
            except Exception as e:
                return {"error": e}

#@TODO add check if user/wallet doesn't exist revert
async def get_wallets(tg_id: int):
    user_pk = await _check_user_exists(tg_id)
    async with Session() as s:
        async with s.begin():
            try:
                user_wallets = await s.execute(
                    select(Wallets).where(Wallets.user_id == user_pk).order_by(Wallets.name)
                )
                return user_wallets.scalars().all()
            except Exception as e:
                raise e


"""connect amazing charge pottery demand alien current churn critic pistol crack debate"""
"""dcda4dc6f971dd612f8c06ee4061f1db36992aa8edbc44737ecc9dee1212a9de"""
