from pydantic import BaseModel, validator
from typing import Union, Optional


"""
Get user settings
change slippage for wallet
make user premium user
ban user
scam protectoin on 
"""

class User(BaseModel):
    tg_id : int 


class UserSettings(User):
    slippage : float    
    is_premium : bool
    is_banned : bool
    enable_notifications : bool


    # @validator("seting")
    # def check_settings(cls, value):
    #     if value == "a":
    #         return 100
    #     return 0