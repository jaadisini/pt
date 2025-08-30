from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo.results import UpdateResult, InsertOneResult
from typing import Union, Optional

class GroupsDB:
    def __init__(self, db):
        self.collection: AsyncIOMotorCollection = db["groups"]

    async def get_group(self, chat_id: Union[int, str]) -> Optional[dict]:
        return await self.collection.find_one({"chat_id": str(chat_id)})
    
    async def add_group(self, chat_id: Union[int, str], state) -> bool:
        chat_id = str(chat_id)
        existing_group = await self.get_group(chat_id)
        if existing_group:
            update_result: UpdateResult = await self.collection.update_one(
                {"chat_id": chat_id},
                {"$set": {"antibc_state": state}},
            )
            return update_result.modified_count > 0
        else:
            insert_result: InsertOneResult = await self.collection.insert_one({
                "chat_id": chat_id,
                "antibc_state": state,
            })
            return insert_result.inserted_id is not None
        
    async def get_antibc_state(self, chat_id: Union[int, str]) -> bool:
        group_info = await self.get_group(str(chat_id))
        return group_info.get('antibc_state', False) if group_info else False

    async def count_all_groups(self) -> int:
        return await self.collection.count_documents({})