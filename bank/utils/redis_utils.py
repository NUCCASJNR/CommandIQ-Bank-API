#!/usr/bin/env python3

"""Contains RedisHandler class"""

import redis
from datetime import datetime, timedelta


class RedisClient:
    """
    Redis Client class
    """

    def __init__(self, host='localhost', port=6379, db=0):
        self.redis_client = redis.StrictRedis(host=host, port=port, db=db)

    def set_key(self, key, value, expiry=None):
        """
        Sets a key in redis
        @param key: The key to set
        @param value: The value to set
        @param expiry: The expiry time in seconds
        """
        try:
            if expiry:
                self.redis_client.set(key, value, ex=expiry)
            else:
                self.redis_client.set(key, value)
            return True
        except redis.RedisError as e:
            print(f"Error setting key '{key}' in Redis: {e}")

    def get_key(self, key):
        """
        Gets a key from redis
        @param key: The key to get
        """
        try:
            return self.redis_client.get(key)
        except redis.RedisError as e:
            print(f"Error getting key '{key}' from Redis: {e}")

    def delete_key(self, key):
        """
        Deletes a key from redis
        @param key: The key to delete
        """
        try:
            self.redis_client.delete(key)
            return True
        except redis.RedisError as e:
            print(f"Error deleting key '{key}' from Redis: {e}")

    def generate_key_name(self, obj) -> object:
        """
        Generates a key name for redis
        @param obj: The object to generate key name for
        """
        return f"{obj.__class__.__name__}:{obj.id}"
