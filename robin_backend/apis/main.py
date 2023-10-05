import sys

sys.path.insert(0, "/home/zeal/Desktop/robin/robin_backend/")
from fastapi import FastAPI
import uvicorn

import os

# correct databse spelling @todo

# Adding the path of the 'database' folder to the system path
from database import engine
from database.models import Users, Wallets, Base
from routers import create_new_wallets, get_change_wallets,buy_tokens, get_token_balances, user_settings



app = FastAPI()


@app.on_event("startup")
async def app_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("shutdown")
async def app_shutdown():
    await engine.dispose()


app.include_router(create_new_wallets.router)
app.include_router(get_change_wallets.router)
app.include_router(buy_tokens.router)
app.include_router(get_token_balances.router)
app.include_router(user_settings.router)
# @app.post("/{_id}/{secret}/{address}")
# async def add_user(_id, secret, address):
#     response = await add_user_when_secret(_id, secret, address)
#     return {"message": response}

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)

