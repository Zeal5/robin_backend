from sqlalchemy.orm import sessionmaker
from .models import *
from . import Session


async def add_user_keys(tg_id, key_value) -> str:
    try:
        session = Session()
        existing_user = session.query(User).filter_by(tg_id=tg_id).first()
        if existing_user:
            keys = get_user_keys(tg_id)
            # print(len(keys))
            new_key = Wallet_Key(key_name=f"Wallet {len(keys) + 1}", key_value=key_value)
            # Establish the relationship between the user and the key
            existing_user.keys.append(new_key)
            session.commit()
            return "New keys added successfully."
        else:
            new_user = User(tg_id=tg_id)
            new_key = Wallet_Key(key_name="Wallet 1", key_value=key_value)
            new_user.keys.append(new_key)
            session.add(new_user)
            session.commit()
            return "New user and keys added successfully."
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
        return "Something wen't wrong"
    finally:
        session.close()

def get_user_keys(tg_id):
    try:
        session = Session()
        keys = session.query(Wallet_Key).join(User,User.id == Wallet_Key.user_id).filter(User.tg_id == tg_id).all()
        if keys:
            return keys
        else :
            return ['no wallets found']
    except Exception as e:
        print(f"Error while getting user keys {e}")
    
    finally:
        session.close()
