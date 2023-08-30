import sys

sys.path.insert(0, "/home/zeal/Desktop/robin/robin_backend/")
from fastapi import FastAPI
import uvicorn

import os

# correct databse spelling @todo

# Adding the path of the 'database' folder to the system path
from database import engine
from database.models import Users, Wallets, Base
from sqlalchemy.ext.asyncio import AsyncSession  # for type checking session
from apis.routers import users,wallets,buy_tokens



app = FastAPI()


@app.on_event("startup")
async def app_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("shutdown")
async def app_shutdown():
    await engine.dispose()


app.include_router(users.router)
app.include_router(wallets.router)
app.include_router(buy_tokens.router)
# @app.post("/{_id}/{secret}/{address}")
# async def add_user(_id, secret, address):
#     response = await add_user_when_secret(_id, secret, address)
#     return {"message": response}

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)

