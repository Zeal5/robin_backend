import sys, os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import pytest
import asyncio
from database.connectionpool import get_connection
from database.queries import add_user_when_secret




@pytest.mark.asyncio
async def test_insert_data():
    user_id = "1www11"
    secret = "sssss"
    address = "11"

    inserted_row_id = await add_user_when_secret(user_id, secret, address)
    assert "successfully" in inserted_row_id
    # assert inserted_row_id is not None

    # Verify that the data is inserted and can be fetched correctly.
    async with get_connection() as conn:
        async with conn.transaction():
            query = f"SELECT * FROM tg_users WHERE user_id = $1"
            fetched_data = await conn.fetch(query, user_id)
            assert fetched_data["user_id"] == user_id
        
        async with conn.transaction():
            querry = """
            SELECT * FROM wallets WHERE tg_user_id = $1
            """
            fetched_data = await conn.fetch(querry, user_id)

        assert fetched_data["secret"] == secret
        assert fetched_data["address"] == address


    
    
