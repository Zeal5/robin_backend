from sqlalchemy import Column, DateTime, String, ForeignKey, Boolean, BIGINT
from sqlalchemy.orm import (
    relationship,
    DeclarativeBase,
    Mapped,
    mapped_column,
)
from typing import Optional


class Base(DeclarativeBase):
    pass


# Define the Users table
"""
id,
tg_id,
keys ( foreign key) 
"""
class Users(Base):
    __tablename__ = "user"
    # id = Column(Integer, primary_key=True)
    # subscribed: Mapped[Optional[bool]] = mapped_column(Boolean, default=False)
    # tester: Mapped[Optional[bool]] = mapped_column(Boolean, default=False)
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(nullable=False, index=True, unique= True)
    keys = relationship("Wallets", back_populates="user")


# Define the Keys table
"""
id,
user_id,
key_name,
kay_value,
user (foreign key0
"""
class Wallets(Base):
    __tablename__ = "wallet"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = Column(BIGINT, ForeignKey("user.id"))
    secret: Mapped[str] = mapped_column(String, nullable=False)
    address: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[Optional[str]] = mapped_column(String)
    user = relationship("Users", back_populates="keys")
