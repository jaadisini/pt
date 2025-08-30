from motor.motor_asyncio import AsyncIOMotorClient
from .groups import GroupsDB
from .users import UsersDB
from .blockwords import BlockwordsDB
from config import CDATABASE

connection = AsyncIOMotorClient(CDATABASE.DATABASE_URL)
database = connection["AuputProtector"]

groupdb = GroupsDB(database)
userdb = UsersDB(database)
blockwordsdb = BlockwordsDB(database)