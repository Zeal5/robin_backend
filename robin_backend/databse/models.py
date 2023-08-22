from sqlalchemy import Column,DateTime, Integer, String, ForeignKey, Boolean, BIGINT
from sqlalchemy.orm import sessionmaker,relationship

from . import Base 

# Define the Users table
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    tg_id = Column(BIGINT,nullable=False,unique=True)
    subscribed = Column(Boolean, default=False)
    tester = Column(Boolean,default=False)
    keys = relationship('Wallet_Key', back_populates='user')



# Define the Keys table
class Wallet_Key(Base):
    __tablename__ = 'keys'
    id = Column(Integer, primary_key=True)
    user_id = Column(BIGINT, ForeignKey('users.id'))
    key_name = Column(String)
    key_value = Column(String,nullable=False)
    user = relationship('User', back_populates='keys')








