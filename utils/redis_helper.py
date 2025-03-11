import redis
import os
from dotenv import load_dotenv

load_dotenv()

class RedisHelper:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=os.getenv("REDIS_HOST"),
            port=int(os.getenv("REDIS_PORT")),
            username="default",
            password="JXYOxc7lUkaJ6ZiwN4LeCOSBBCBBb5zF",
            decode_responses=True
        )

    def set_otp(self, username: str, otp: str, expiry: int = 300):
        self.redis_client.setex(f"otp:{username}", expiry, otp)

    def get_otp(self, username: str):
        return self.redis_client.get(f"otp:{username}")

    def delete_otp(self, username: str):
        self.redis_client.delete(f"otp:{username}")

redis_helper = RedisHelper()