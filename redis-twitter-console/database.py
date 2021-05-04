"""This module is to configure our database."""

from dotenv import dotenv_values, find_dotenv
from redis import Redis, StrictRedis


def flush_database(redis: Redis) -> None:
    """Flushes our database."""
    redis.flushdb()
    print("Database flushed!")


def get_all_data(redis: Redis) -> None:
    """Gets all data that are available at your Redis instance."""
    strings = []
    hashes = []
    zsets = []
    lists = []
    sets = []

    keys = redis.keys("*")
    print(f"Keys available: {keys}", end="\n")

    for key in keys:
        redis_type = redis.type(key)

        if redis_type == "string":
            vals = redis.get(key)
            strings.append(f"Key is '{key}' - Data type is string: {vals}")

        if redis_type == "hash":
            vals = redis.hgetall(key)
            hashes.append(f"Key is '{key}' - Data type is hash: {vals}")

        if redis_type == "zset":
            vals = redis.zrange(key, 0, -1)
            zsets.append(f"Key is '{key}' - Data type is sorted set: {vals}")

        if redis_type == "list":
            vals = redis.lrange(key, 0, -1)
            lists.append(f"Key is '{key}' - Data type is list: {vals}")

        if redis_type == "set":
            vals = redis.smembers(key)
            sets.append(f"Key is '{key}' - Data type is set: {vals}")

    print("\nStrings: ")
    for item in strings:
        print(item)

    print("\nHashes: ")
    for item in hashes:
        print(item)

    print("\nZsets: ")
    for item in zsets:
        print(item)

    print("\nLists: ")
    for item in lists:
        print(item)

    print("\nSets: ")
    for item in sets:
        print(item)


def redis_init() -> Redis:
    """Initializes Redis session."""
    config = dotenv_values(find_dotenv())

    redis = StrictRedis(
        host=config["REDIS_HOST"],
        port=config["REDIS_PORT"],
        password=config["REDIS_PASSWORD"],
        decode_responses=True,
    )

    return redis
