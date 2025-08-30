from typing import Union, List, Optional
from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo.results import UpdateResult, InsertOneResult, DeleteResult

class BlockwordsDB:
    def __init__(self, db):
        self.collection: AsyncIOMotorCollection = db["blockwords"]

    async def get_chat(self, chat_id: Union[int, str]) -> Optional[dict]:
        return await self.collection.find_one({"chat_id": str(chat_id)})

    async def add_blockword(self, chat_id: Union[int, str], word: str) -> bool:
        chat_id = str(chat_id)
        update_result: UpdateResult = await self.collection.update_one(
            {"chat_id": chat_id},
            {"$addToSet": {"blockwords": word.lower()}},
            upsert=True
        )
        return update_result.modified_count > 0 or update_result.upserted_id is not None

    async def remove_blockword(self, chat_id: Union[int, str], word: str) -> bool:
        chat_id = str(chat_id)
        update_result: UpdateResult = await self.collection.update_one(
            {"chat_id": chat_id},
            {"$pull": {"blockwords": word.lower()}}
        )
        return update_result.modified_count > 0

    async def get_blockwords(self, chat_id: Union[int, str]) -> List[str]:
        chat_data = await self.get_chat(str(chat_id))
        return chat_data.get('blockwords', []) if chat_data else []

    async def is_blocked(self, chat_id: Union[int, str], word: str) -> bool:
        blockwords = await self.get_blockwords(str(chat_id))
        return word.lower() in blockwords

    async def clear_blockwords(self, chat_id: Union[int, str]) -> bool:
        update_result: UpdateResult = await self.collection.update_one(
            {"chat_id": str(chat_id)},
            {"$set": {"blockwords": []}}
        )
        return update_result.modified_count > 0