import redis.asyncio as redis
import os
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))

redis_client = redis.Redis(
    host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)


async def cache_token(token: str, user_id: int, ttl_seconds: int = 5):
    await redis_client.set(token, user_id, ex=ttl_seconds)


async def get_user_id_from_token(token: str):
    return await redis_client.get(token)
