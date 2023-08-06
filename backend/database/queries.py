from .connectionpool import get_connection
from asyncpg.exceptions import ForeignKeyViolationError, UniqueViolationError


async def add_user_when_secret(user_id: str, secret: str, address: str) -> str:
    print("adding user " + user_id)
    async with get_connection() as conn:
        try:
            # Check if user is already in db
            async with conn.transaction():
                check_user_if_exists = await conn.fetchval(
                    """
                                                                SELECT user_id FROM tg_users WHERE 
                                                                user_id = $1 """,
                    user_id,
                )
            if check_user_if_exists:
                # If user already exists check if wallet already exists
                async with conn.transaction():
                    check_wallet_if_exists = await conn.fetchval(
                        """
                                                                SELECT secret_key FROM wallets WHERE 
                                                                secret_key = $1 """,
                        secret,
                    )
                if check_wallet_if_exists:
                    # If user and wallet already exists return
                    return "Secret key and user already exists in wallets table successfully."
                else:
                    # If user exists and wallet does not exist add wallet
                    async with conn.transaction():
                        user_pk_from_tg_id = await conn.fetchval(
                            """
                        SELECT id FROM tg_users WHERE user_id = $1
                                                                """,
                            user_id,
                        )

                    add_wallet_query = """
                                    INSERT INTO wallets (secret_key, address, tg_user_id)
                                    VALUES ($1, $2, $3)"""
                    async with conn.transaction():
                        await conn.execute(
                            add_wallet_query, secret, address, user_pk_from_tg_id
                        )
                    return "Wallet added successfully."
            else:
                # If user does not exist then add wallet and user

                add_user_query = """
                INSERT INTO tg_users (user_id)
                VALUES ($1)
                """
                async with conn.transaction():
                    await conn.execute(add_user_query, user_id)

                async with conn.transaction():
                    user_pk_from_tg_id = await conn.fetchval(
                        """
                    SELECT id FROM tg_users WHERE user_id = $1
                                                            """,
                        user_id,
                    )

                add_wallet_query = """
                                    INSERT INTO wallets (secret_key, address, tg_user_id)
                                    VALUES ($1, $2, $3)"""
                async with conn.transaction():
                    await conn.execute(
                        add_wallet_query, secret, address, user_pk_from_tg_id
                    )
                return "User added successfully."

        except UniqueViolationError:
            return "User ID already exists in tg_users table."
        except ForeignKeyViolationError:
            return (
                "Foreign key violation. Make sure the user_id exists in tg_users table."
            )
        except Exception as e:
            return "An unexpected error occurred:", str(e)


