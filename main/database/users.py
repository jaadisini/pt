from typing import Union, List, Optional
from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo.results import UpdateResult, InsertOneResult, DeleteResult

class UsersDB:
    def __init__(self, db):
        self.collection: AsyncIOMotorCollection = db["users"]

    async def get_user(self, chat_id: Union[int, str]) -> Optional[dict]:
        return await self.collection.find_one({"chat_id": str(chat_id)})

    async def create_user(self, chat_id: Union[int, str]) -> bool:
        chat_id = str(chat_id)
        existing_user = await self.get_user(chat_id)
        if not existing_user:
            insert_result: InsertOneResult = await self.collection.insert_one({
                "chat_id": chat_id,
                "user_blacklist": [],
                "user_whitelist": []
            })
            return insert_result.inserted_id is not None
        return False

    async def add_to_blacklist(self, chat_id: Union[int, str], user_id: Union[int, str]) -> bool:
        chat_id, user_id = str(chat_id), str(user_id)
        update_result: UpdateResult = await self.collection.update_one(
            {"chat_id": chat_id},
            {"$addToSet": {"user_blacklist": user_id}},
            upsert=True
        )
        return update_result.modified_count > 0 or update_result.upserted_id is not None

    async def remove_from_blacklist(self, chat_id: Union[int, str], user_id: Union[int, str]) -> bool:
        chat_id, user_id = str(chat_id), str(user_id)
        update_result: UpdateResult = await self.collection.update_one(
            {"chat_id": chat_id},
            {"$pull": {"user_blacklist": user_id}}
        )
        return update_result.modified_count > 0

    async def add_to_whitelist(self, chat_id: Union[int, str], user_id: Union[int, str]) -> bool:
        chat_id, user_id = str(chat_id), str(user_id)
        update_result: UpdateResult = await self.collection.update_one(
            {"chat_id": chat_id},
            {"$addToSet": {"user_whitelist": user_id}},
            upsert=True
        )
        return update_result.modified_count > 0 or update_result.upserted_id is not None

    async def remove_from_whitelist(self, chat_id: Union[int, str], user_id: Union[int, str]) -> bool:
        chat_id, user_id = str(chat_id), str(user_id)
        update_result: UpdateResult = await self.collection.update_one(
            {"chat_id": chat_id},
            {"$pull": {"user_whitelist": user_id}}
        )
        return update_result.modified_count > 0

    async def get_blacklist(self, chat_id: Union[int, str]) -> List[str]:
        user_data = await self.get_user(str(chat_id))
        return user_data.get('user_blacklist', []) if user_data else []

    async def get_whitelist(self, chat_id: Union[int, str]) -> List[str]:
        user_data = await self.get_user(str(chat_id))
        return user_data.get('user_whitelist', []) if user_data else []

    async def is_blacklisted(self, chat_id: Union[int, str], user_id: Union[int, str]) -> bool:
        blacklist = await self.get_blacklist(str(chat_id))
        return str(user_id) in blacklist

    async def is_whitelisted(self, chat_id: Union[int, str], user_id: Union[int, str]) -> bool:
        whitelist = await self.get_whitelist(str(chat_id))
        return str(user_id) in whitelist

    async def clear_blacklist(self, chat_id: Union[int, str]) -> bool:
        update_result: UpdateResult = await self.collection.update_one(
            {"chat_id": str(chat_id)},
            {"$set": {"user_blacklist": []}}
        )
        return update_result.modified_count > 0

    async def clear_whitelist(self, chat_id: Union[int, str]) -> bool:
        update_result: UpdateResult = await self.collection.update_one(
            {"chat_id": str(chat_id)},
            {"$set": {"user_whitelist": []}}
        )
        return update_result.modified_count > 0