import os
import redis
from dotenv import load_dotenv

load_dotenv()
redis_client = redis.Redis.from_url(os.getenv('REDIS_HOST'))

redis_client.set("test", "working")
print(redis_client.get("test"))