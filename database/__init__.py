from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from sqlalchemy.orm import sessionmaker


engine = create_async_engine(
    f"postgresql+asyncpg://postgres:zeal@127.0.0.1:5432/robin")

Session = sessionmaker(bind=engine, class_=AsyncSession,
                       expire_on_commit=False)
