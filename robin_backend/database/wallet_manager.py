from .models import Users, Wallets
from . import Session
from sqlalchemy.future import select
from sqlalchemy import insert

async def check_user_exists(_id:int) -> bool:
    """ Checks if user with tg_id exists in database

    Args:
        ``tg_id``: The Telegram ID of user
    
    Returns:
        ``bool`` : True if user with tg_id exists
    """
    async with Session() as s:
        async with s.begin():
            users = await s.execute(select(Users).where(Users.tg_id == _id))
            return True if users.scalars().first() else False




async def add_user_keys(tg_id) -> bool:
    """Add user, wallets to the database.

    Args:
        ``tg_id`` : The Telegram ID of the user.\n
        ``secret`` : The secret Key for Wallet authentication

    Returns:
        ``Bool``: True if user and wallet was added successfully.
    """

    async with Session() as s:
        async with s.begin():
            # user =  await s.execute(select(User).where(User.tg_id == tg_id))
            stmt = insert(Users).values(tg_id =tg_id)
            await s.execute(stmt)

    





"""connect amazing charge pottery demand alien current churn critic pistol crack debate"""
"""dcda4dc6f971dd612f8c06ee4061f1db36992aa8edbc44737ecc9dee1212a9de"""