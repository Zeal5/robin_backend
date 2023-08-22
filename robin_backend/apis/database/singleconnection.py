import asyncpg
from contextlib import asynccontextmanager


@asynccontextmanager
async def get_single_connection():
    hostname = "192.168.56.1"
    database_name = "robin"
    port = 5432
    owner = "postgres"
    password = "zeal"

    conn = None
    try:
        conn = await asyncpg.connect(
                            host=hostname,
                            port=port, 
                            database=database_name, 
                            user=owner, 
                            password=password,
        )
        yield conn

    except Exception as e:
        print(e)
    finally:
        if conn is not None:
            await conn.close()


