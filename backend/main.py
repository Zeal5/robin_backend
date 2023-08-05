from fastapi import FastAPI

from database.connectionpool import get_connection, on_shutdown

import os
app = FastAPI()

hostname = "192.168.56.1"
database_name = "robin"
port = 5432
owner = "postgres"
password = "zeal"

@app.on_event("startup")
async def app_startup():
    root_folder = os.path.dirname(os.path.abspath(__file__))
    schema_file = f"{os.path.join(root_folder,'database/schema.sql')}"
    with open(schema_file, 'r') as file:
        schema_sql = file.read()
        async with get_connection() as conn:
            await conn.execute(schema_sql)
            print("table schema created successfully")


@app.on_event("shutdown")
async def app_shutdown():
    await on_shutdown()


@app.get("/{id}")
async def read_root(id:int):
    print(f"Received request ID: {id}")
    async with get_connection() as conn:
        async with conn.transaction():
            query = "SELECT * FROM users"
            result = await conn.fetch(query)
            data = [dict(row) for row in result]

            return {"message": data}


