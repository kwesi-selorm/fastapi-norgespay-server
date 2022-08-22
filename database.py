import os

import motor.motor_asyncio
from beanie import init_beanie
from dotenv import load_dotenv

from models import Salary, User, DBContributor

load_dotenv()


async def init_db():
    connection_str = os.getenv("MONGODB_URI")
    client = motor.motor_asyncio.AsyncIOMotorClient(connection_str)

    await init_beanie(
        database=client.test, document_models=[Salary, User, DBContributor]
    )
