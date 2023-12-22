import redis.asyncio as aioredis
from core.config import SETTINGS


rate_limit_redis = aioredis.from_url(url=SETTINGS.RATE_LIMIT_REDIS_HOST, decode_responses=True)

scheduler_redis = aioredis.from_url(url=SETTINGS.SCHEDULER_REDIS_HOST, decode_responses=True)
