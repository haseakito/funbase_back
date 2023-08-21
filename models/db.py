from prisma import Prisma
from fastapi import status, HTTPException

"""
Function handling the database connection
"""
async def get_db():
    db = Prisma(auto_register=True)
    try:
        await db.connect()
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await db.disconnect()