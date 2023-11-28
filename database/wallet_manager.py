from .models import Users, Wallets, ActiveWallets, UserSettings
from . import Session
from sqlalchemy.future import select
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import insert, exists, update
from sqlalchemy.orm import joinedload
import functools
from typing import Union

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
            print("keys more then 7")
            return {"detail": "Max 7 wallets are allowed"}

    return wraped


async def _check_user_exists(_id: int) -> Union[bool, int]:
    """Checks if user with tg_id exists in database

    Args:
        ``tg_id``: The Telegram ID of user

    Returns:
        ``bool`` : user pk if user with tg_id exists else False
    """
    async with Session() as s:
        async with s.begin():
            try:
                users = await s.execute(select(Users).filter(Users.tg_id == _id))
                return users.scalar_one().id
            except NoResultFound as e:
                return False


async def check_wallet_exists_for_user(_id: int, secret: str) -> dict:
    if not secret.startswith('0x'):
        secret = '0x' + secret
    return_dict = {"user": False, "wallet": False}
    user_id: int = await _check_user_exists(_id)
    if not user_id:
        return return_dict
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


async def add_user_and_keys(
    tg_id: int, secret: str, address: str, wallet_name: str
) -> bool | dict:
    """Add user, wallets to the database.

    Args:
        ``tg_id`` : The Telegram ID of the user.\n
        ``secret`` : The secret Key for Wallet authentication

    Returns:
        ``Bool``: True if user and wallet was added successfully.
    """
    print("running add user and keys?")
    async with Session() as s:
        async with s.begin():
            try:
                new_user = Users(tg_id=tg_id)
                new_wallet = Wallets(
                    user=new_user, secret=secret, address=address, name=wallet_name
                )
                s.add(new_user)
                s.add(new_wallet)
                await s.flush()
                print(f"new user = {new_user.id}")
                print(f"new_wallet = {new_wallet.id}")
                new_active_wallet = ActiveWallets(
                    user_id=new_user.id, wallet_id=new_wallet.id
                )
                settings = UserSettings(slippage=9, user_id=new_user.id)
                s.add(new_active_wallet)
                s.add(settings)
                await s.commit()
                return True
            except Exception as e:
                raise e


@get_wallets_count
async def add_keys_when_user(
    tg_id: int, secret: str, address: str, wallet_name: str
) -> bool | dict:
    async with Session() as s:
        async with s.begin():
            try:
                existing_user = await s.execute(
                    select(Users).filter(Users.tg_id == tg_id)
                )
                user_id = existing_user.scalars().one().id
                # user = existing_user.scalar_one()
                wallet = Wallets(
                    user_id=user_id, secret=secret, address=address, name=wallet_name
                )
                s.add(wallet)
                await s.commit()
                return True
            except Exception as e:
                return str(e)


# @TODO add check if user/wallet doesn't exist revert
async def get_wallets(tg_id: int) -> list:
    """takes in tg_id of any user and returns the list \n
    of all the wallets orderd by wallet name\n
    (default wallet names are wallet1,wallet2...)\n
    `args:`
        `tg_id:` user tg_id int
    `Returns:`
        List of wallet objects
    """

    user_pk = await _check_user_exists(tg_id)
    print(f"user pk = {user_pk}")
    async with Session() as s:
        async with s.begin():
            try:
                user_wallets = await s.execute(
                    select(Wallets)
                    .where(Wallets.user_id == user_pk)
                    .order_by(Wallets.name)
                )
                return user_wallets.scalars().all()
            except Exception as e:
                raise e


async def get_active_wallets_id(tg_id: str) -> int:
    user_pk = await _check_user_exists(tg_id)
    async with Session() as s:
        async with s.begin():
            try:
                user_wallets = await s.execute(
                    select(ActiveWallets).filter(
                        ActiveWallets.user_id == user_pk)
                )
                return user_wallets.scalar_one().wallet_id

            except Exception as e:
                raise e


async def get_slippage(user_id: int) -> int:
    """takes in foreign key reference(not the tg_id) from user table and returns sliippage"""
    async with Session() as s:
        async with s.begin():
            try:
                user_wallets = await s.execute(
                    select(UserSettings).filter(
                        UserSettings.user_id == user_id)
                )
                return user_wallets.scalar_one().slippage

            except Exception as e:
                raise e


async def get_active_wallet(tg_id: str) -> int:
    try:
        wallet_id = await get_active_wallets_id(tg_id)
        print(f"wallet id{wallet_id}")
        async with Session() as s:
            async with s.begin():
                user_wallet = await s.execute(
                    select(Wallets).filter(Wallets.id == wallet_id)
                )
                return user_wallet.scalars().first()

    except Exception as e:
        raise e


async def change_active_wallet(tg_id: int, active_wallet_id: int) -> bool:
    user_pk = await _check_user_exists(tg_id)
    print(f"user pk = {user_pk}")
    async with Session() as s:
        async with s.begin():
            try:
                stmt = (
                    update(ActiveWallets)
                    .where(ActiveWallets.user_id == user_pk)
                    .values(wallet_id=active_wallet_id)
                )
                await s.execute(stmt)
                await s.commit()
                return True
            except Exception as e:
                raise e


async def test(tg_id: int):
    # user_pk = await _check_user_exists(tg_id)
    # print(f"user pk = {user_pk}")
    async with Session() as s:
        async with s.begin():
            try:
                # x = await s.execute(select(UserSettings).where(UserSettings.user_id == user_pk))
                # print(x)
                # y = x.scalars().first()

                # print(y.slippage)
                user_settings = await s.execute(select(Users).options(joinedload(Users.settings)).filter(Users.tg_id == tg_id))
                settings = user_settings.scalars().first().settings

                # z =  x.settings
                return settings
            except Exception as e:
                print(str(e))


"""connect amazing charge pottery demand alien current churn critic pistol crack debate"""
"""dcda4dc6f971dd612f8c06ee4061f1db36992aa8edbc44737ecc9dee1212a9de"""
