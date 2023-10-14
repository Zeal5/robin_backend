from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


ip = "192.168.56.1"
engine = create_async_engine(f"postgresql+asyncpg://postgres:zeal@{ip}:5432/robin")

Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
