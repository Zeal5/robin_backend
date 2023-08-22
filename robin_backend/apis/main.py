from fastapi import FastAPI

from database.connectionpool import get_connection, on_shutdown
from database.queries import add_user_when_secret
import os

app = FastAPI()







@app.on_event("startup")
async def app_startup():
    root_folder = os.path.dirname(os.path.abspath(__file__))
    schema_file = f"{os.path.join(root_folder,'database/schema.sql')}"
    with open(schema_file, "r") as file:
        schema_sql = file.read()
        async with get_connection() as conn:
            await conn.execute(schema_sql)
            print("table schema created successfully")


@app.on_event("shutdown")
async def app_shutdown():
    await on_shutdown()


@app.get("/")
async def read_root():
    async with get_connection() as conn:
        async with conn.transaction():
            query = "SELECT * FROM users"
            result = await conn.fetch(query)
            data = [dict(row) for row in result]

            return {"message": data}


@app.post("/{_id}/{secret}/{address}")
async def add_user(_id, secret, address):
    response = await add_user_when_secret(_id, secret, address)
    return {"message": response}
