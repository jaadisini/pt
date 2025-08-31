from typing import Union, List, Optional
from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo.results import UpdateResult, InsertOneResult, DeleteResult


class UsersDB:
    def __init__(self, db):
        # semua user blacklist & whitelist disimpan global
        self.collection: AsyncIOMotorCollection = db["global_users"]

    async def init_global(self) -> bool:
        """Inisialisasi dokumen global kalau belum ada"""
        existing = await self.collection.find_one({"_id": "global"})
        if not existing:
            insert_result: InsertOneResult = await self.collection.insert_one({
                "_id": "global",
                "user_blacklist": [],
                "user_whitelist": []
            })
            return insert_result.inserted_id is not None
        return False

    async def add_to_blacklist(self, user_id: Union[int, str]) -> bool:
        user_id = str(user_id)
        await self.init_global()
        update_result: UpdateResult = await self.collection.update_one(
            {"_id": "global"},
            {"$addToSet": {"user_blacklist": user_id}}
        )
        return update_result.modified_count > 0

    async def remove_from_blacklist(self, user_id: Union[int, str]) -> bool:
        user_id = str(user_id)
        await self.init_global()
        update_result: UpdateResult = await self.collection.update_one(
            {"_id": "global"},
            {"$pull": {"user_blacklist": user_id}}
        )
        return update_result.modified_count > 0

    async def add_to_whitelist(self, user_id: Union[int, str]) -> bool:
        user_id = str(user_id)
        await self.init_global()
        update_result: UpdateResult = await self.collection.update_one(
            {"_id": "global"},
            {"$addToSet": {"user_whitelist": user_id}}
        )
        return update_result.modified_count > 0

    async def remove_from_whitelist(self, user_id: Union[int, str]) -> bool:
        user_id = str(user_id)
        await self.init_global()
        update_result: UpdateResult = await self.collection.update_one(
            {"_id": "global"},
            {"$pull": {"user_whitelist": user_id}}
        )
        return update_result.modified_count > 0

    async def get_blacklist(self) -> List[str]:
        await self.init_global()
        data = await self.collection.find_one({"_id": "global"})
        return data.get("user_blacklist", []) if data else []

    async def get_whitelist(self) -> List[str]:
        await self.init_global()
        data = await self.collection.find_one({"_id": "global"})
        return data.get("user_whitelist", []) if data else []

    async def is_blacklisted(self, user_id: Union[int, str]) -> bool:
        bl = await self.get_blacklist()
        return str(user_id) in bl

    async def is_whitelisted(self, user_id: Union[int, str]) -> bool:
        wl = await self.get_whitelist()
        return str(user_id) in wl

    async def clear_blacklist(self) -> bool:
        await self.init_global()
        update_result: UpdateResult = await self.collection.update_one(
            {"_id": "global"},
            {"$set": {"user_blacklist": []}}
        )
        return update_result.modified_count > 0

    async def clear_whitelist(self) -> bool:
        await self.init_global()
        update_result: UpdateResult = await self.collection.update_one(
            {"_id": "global"},
            {"$set": {"user_whitelist": []}}
        )
        return update_result.modified_count > 0
