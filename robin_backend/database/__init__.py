from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


ip = "192.168.56.1"
engine = create_async_engine(f'postgresql+asyncpg://postgres:zeal@{ip}:5432/robin')
# Base = declarative_base()


# Import the model definition here
# from .models import *
# Base.metadata.create_all(engine)

# Create a session for database operations
Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
