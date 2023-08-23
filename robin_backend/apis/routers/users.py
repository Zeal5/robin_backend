from database.wallet_manager import add_user_keys, check_user_exists
from fastapi import APIRouter

from pydantic import BaseModel

router = APIRouter()

class Item(BaseModel):
    id: int


# This function is called to add users and keys to the database
@router.post(path = '/')
async def read_root(item:Item):
    if await check_user_exists(item.id):
        return "User already exists"
    
    new_id = await add_user_keys(int(item.id))
    


