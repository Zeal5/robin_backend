from sqlalchemy import (
    Column,
    DateTime,
    String,
    ForeignKey,
    Boolean,
    BIGINT,
    Integer,
    Float,
    CheckConstraint,
    UniqueConstraint,
)
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
wallets ( foreign key) 
"""


class Users(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id  = mapped_column(BIGINT,nullable=False, index=True, unique=True)

    wallets = relationship(
        "Wallets", backref="user", uselist=True, cascade="all, delete-orphan"
    )
    active_wallet = relationship(
        "ActiveWallets", backref="user", uselist=False, cascade="all, delete-orphan"
    )
    settings = relationship(
        "UserSettings", backref="user", uselist=False, cascade="all, delete-orphan"
    )
    tokens = relationship(
        "TokensBought", backref="user", uselist=True, cascade="all, delete-orphan"
    )


class UserSettings(Base):
    __tablename__ = "user_settings"

    id: Mapped[int] = mapped_column(primary_key=True)
    slippage: Mapped[float] = mapped_column(Float, default=7)
    is_premium: Mapped[bool] = mapped_column(Boolean, default=False)
    is_banned: Mapped[bool] = mapped_column(Boolean, default=False)
    enable_notifications: Mapped[bool] = mapped_column(Boolean, default=True)

    user_id = Column(Integer, ForeignKey("user.id"),unique=True)
    # user = relationship("Users", back_populates="settings")

    # contraints
    __table_args__ = (
        CheckConstraint(
            "slippage >= 0 AND slippage <= 100", name="check_my_float_range"
        ),
    )



class Wallets(Base):
    __tablename__ = "wallet"

    id: Mapped[int] = mapped_column(primary_key=True)
    secret: Mapped[str] = mapped_column(String, nullable=False)
    address: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[Optional[str]] = mapped_column(String)

    user_id = Column(BIGINT, ForeignKey("user.id"))
    # user = relationship("Users", back_populates="wallets")
    active_wallet = relationship(
        "ActiveWallets", backref="wallet", uselist=False
    )
    __table_args__ = (UniqueConstraint("secret", "address", name="uix_secret_address"),)


class ActiveWallets(Base):
    __tablename__ = "active_wallet"
    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = Column(Integer, ForeignKey("user.id"),unique=True)
    wallet_id: Mapped[int] = Column(Integer, ForeignKey("wallet.id"),unique=True)

    # user = relationship("Users", back_populates="active_wallet")
    # wallet = relationship("Wallets", back_populates="active_wallet")



class TokensBought(Base):
    __tablename__ = "tokens_list"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = Column(Integer, ForeignKey("user.id"))
    token_name: Mapped[str] = Column(String)
    token_address: Mapped[str] = Column(String)

    # user = relationship("Users", back_populates="tokens")



"""
-- INSERT INTO public."user" (tg_id) VALUES (123);

-- insert into public."user_settings" (slippage, user_id, is_premium, is_banned, enable_notifications ) 
-- VALUES (2, 1, True, False, True);

-- insert into public."wallet" (secret, address, name, user_id) 
-- VALUES ('gp','ij', 'n', 1);

insert into public."active_wallet" (user_id, wallet_id) 
VALUES (1,1);
"""
