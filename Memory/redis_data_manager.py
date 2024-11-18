import redis
import json
from typing import Optional, Any


class RedisJsonManager:
    def __init__(self, host: str = 'localhost', port: int = 6379, db: int = 0):
        """Initialize Redis connection"""
        self.redis_client = redis.Redis(host=host, port=port, db=db, decode_responses=True)

    def create(self, key: str, data: dict) -> bool:
        """Create a new JSON entry"""
        try:
            if self.redis_client.exists(key):
                return False
            return self.redis_client.set(key, json.dumps(data))
        except Exception as e:
            print(f"Error creating data: {e}")
            return False

    def read(self, key: str) -> Optional[dict]:
        """Read JSON data for a key"""
        try:
            data = self.redis_client.get(key)
            return json.loads(data) if data else None
        except Exception as e:
            print(f"Error reading data: {e}")
            return None

    def update(self, key: str, data: dict) -> bool:
        """Update JSON data for a key"""
        try:
            if not self.redis_client.exists(key):
                return False
            return self.redis_client.set(key, json.dumps(data))
        except Exception as e:
            print(f"Error updating data: {e}")
            return False

    def delete(self, key: str) -> bool:
        """Delete data for a key"""
        try:
            return bool(self.redis_client.delete(key))
        except Exception as e:
            print(f"Error deleting data: {e}")
            return False