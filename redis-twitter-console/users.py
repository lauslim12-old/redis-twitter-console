"""This module is to manage our users."""

from time import time

from redis import Redis

from errors import (
    DuplicateUserError,
    EmptyInputError,
    FollowError,
    UserDoesNotExistError,
    UserIsNotYourFollowingError,
)
from utils import is_string_blank


def follow(redis: Redis, uid: int) -> None:
    """Follows another user.

    Algorithm:
    ----------
    1. Enter the username of someone that one wants to follow.
    2. Sanity check, if the string is blank, raise an exception.
    3. Check if user ID exists.
    4. Fetch the user id from 'users' hash.
    5. If the current user wants to follow themselves, then raise an exception.
    6. Create a mapping to store data in zset (sorted set).
    7. Store 'following' and 'followers' with the suitable IDs.

    Parameters:
    -----------
    redis (Redis): Redis instance
    uid (int): User id

    Returns:
    --------
    None
    """
    follow_username = input("Enter the username of someone to follow: ")

    if is_string_blank(follow_username):
        raise EmptyInputError()

    if not redis.hexists("users", follow_username):
        raise UserDoesNotExistError()

    user_id_to_be_followed = redis.hget("users", follow_username)

    if user_id_to_be_followed == uid:
        raise FollowError()

    following_mapping = {user_id_to_be_followed: int(time())}
    followers_mapping = {uid: int(time())}

    redis.zadd(f"following:{uid}", following_mapping)
    redis.zadd(f"followers:{user_id_to_be_followed}", followers_mapping)

    print(f"You have successfully followed {follow_username}")


def logout() -> False:
    """Logs out a user."""
    print("You have been logged out!")
    return False


def other_profile(redis: Redis) -> None:
    """Try to look at other people's profile.

    Algorithm:
    ----------
    1. Take input of username.
    2. Sanity check, if blank raise an exception.
    3. Check if user exists.
    4. Fetch the 'user_id' in 'users' HSET.
    5. Fetch the user's data in 'user' HSET.
    6. Display our data.

    Parameters:
    -----------
    redis (Redis): Redis instance

    Returns:
    --------
    None
    """
    target_username = input("Enter the username that you want to see: ")

    if is_string_blank(target_username):
        raise EmptyInputError()

    if not redis.hget("users", target_username):
        raise UserDoesNotExistError()

    uid = redis.hget("users", target_username)
    user_data = redis.hgetall(f"user:{uid}")
    tweet_data = redis.lrange(f"tweet_user:{uid}", 0, -1)
    following_data = redis.zrange(f"following:{uid}", 0, -1)
    followers_data = redis.zrange(f"followers:{uid}", 0, -1)

    print("Their personal data:")
    print(user_data)

    print("\nTheir tweets:")
    for item in tweet_data:
        post = redis.hgetall(f"tweet:{item}")
        print(post)

    print("\nTheir following:")
    for item in following_data:
        user = redis.hgetall(f"user:{item}")
        print(user)

    print("\nTheir followers:")
    for item in followers_data:
        user = redis.hgetall(f"user:{item}")
        print(user)


def profile(redis: Redis, uid: int) -> None:
    """Get personal data according to the session key.

    Algorithm:
    ----------
    1. Get all user's data from 'user' hash (intentionally hide passwords).
    2. Get all user's tweets from 'tweet_user' list.
    3. Get all user's following data from 'following' sorted set.
    4. Get all user's followers data from 'followers' sorted set.
    5. Display data in the screen.

    Parameters:
    -----------
    redis (Redis): Redis instance
    uid (int): User id

    Returns:
    --------
    None
    """
    user_data = redis.hgetall(f"user:{uid}")
    tweet_data = redis.lrange(f"tweet_user:{uid}", 0, -1)
    following_data = redis.zrange(f"following:{uid}", 0, -1)
    followers_data = redis.zrange(f"followers:{uid}", 0, -1)

    print("My personal data:")

    user_data.pop("password", "secret")
    print(user_data)

    print("\nMy tweets:")
    for item in tweet_data:
        post = redis.hgetall(f"tweet:{item}")
        print(post)

    print("\nMy following:")
    for item in following_data:
        user = redis.hgetall(f"user:{item}")
        print(user)

    print("\nMy followers:")
    for item in followers_data:
        user = redis.hgetall(f"user:{item}")
        print(user)


def timeline(redis: Redis) -> None:
    """Gets the global timeline of what's happening in the world.

    Algorithm:
    ----------
    1. Get all recent tweets.

    Parameters:
    ----------
    redis (Redis): Redis instance

    Returns:
    --------
    None
    """
    recent_tweets_list = redis.lrange("timeline", 0, 1000)

    print("All recent tweets: ")
    for item in recent_tweets_list:
        post = redis.hgetall(f"tweet:{item}")
        print(post)


def tweet(redis: Redis, uid: int) -> None:
    """Send a tweet connected to the user's account.

    Algorithm:
    ----------
    1. Get tweet.
    2. Sanity check, if tweet is blank, raise an exception.
    3. Increment 'tweet_id', as it is a standalone entity.
    4. Store our tweet data in a HSET.
    5. Store our tweet identifier for a certain user in LPUSH (list).
    6. Store the reference to the tweet in an LPUSH (list) for the global timeline.
    7. Trim the 'timeline' Redis list to the latest 1000 tweet references.

    Parameters:
    -----------
    redis (Redis): Redis instance
    uid (int): User id

    Returns:
    --------
    None
    """
    content = input("What's on your mind: ")

    if is_string_blank(content):
        raise EmptyInputError()

    tweet_data = {
        "uid": uid,
        "content": content,
        "date_posted": int(time()),
        "date_modified": int(time()),
    }

    tweet_id = redis.incr("next_tweet_id")
    redis.hset(f"tweet:{tweet_id}", mapping=tweet_data)
    redis.lpush(f"tweet_user:{uid}", tweet_id)
    redis.lpush("timeline", tweet_id)
    redis.ltrim("timeline", 0, 1000)

    print("Tweet has been successfully inserted!")


def unfollow(redis: Redis, uid: int) -> None:
    """Unfollows a user.

    Algorithm:
    ----------
    1. Get the sorted set of the user.
    2. Sanity check, if the user id is blank, raise an exception.
    3. Get the targeted user ID.
    4. If user does not exist, raise an exception.
    5. If targeted user is not in the 'following' of the current user, raise an exception.
    6. Remove from the sorted set of the current user, and change the suitable followers/following.

    Parameters:
    -----------
    redis (Redis): Redis instance
    uid (int): User id

    Returns:
    -------
    None
    """
    username_to_be_unfollowed = input("Enter the username that you want to unfollow: ")
    user_id_to_be_unfollowed = redis.hget("users", username_to_be_unfollowed)

    if is_string_blank(username_to_be_unfollowed):
        raise EmptyInputError()

    if not user_id_to_be_unfollowed:
        raise UserDoesNotExistError()

    if not redis.zscore(f"following:{uid}", user_id_to_be_unfollowed):
        raise UserIsNotYourFollowingError()

    redis.zrem(f"following:{uid}", user_id_to_be_unfollowed)
    redis.zrem(f"followers:{user_id_to_be_unfollowed}", uid)

    print(
        f"You have succesfully unfollowed a person with username {username_to_be_unfollowed}!"
    )


def update_profile(redis: Redis, uid: int) -> None:
    """Updates a user.

    Algorithm:
    ----------
    1. Get the input.
    2. Sanity checks.
    3. Check for duplicate username.
    4. Update the hash for 'user:id'.

    Parameters:
    -----------
    redis (Redis): Redis instance
    uid (int): User id

    Returns:
    --------
    """
    new_username = input("Enter your new username here: ")

    if is_string_blank(new_username):
        raise EmptyInputError()

    if redis.hexists("users", new_username):
        raise DuplicateUserError()

    new_user_data = {"username": new_username, "modification_date": int(time())}
    old_username = redis.hget(f"user:{uid}", "username")

    redis.hset(f"user:{uid}", mapping=new_user_data)
    redis.hdel("users", old_username)
    redis.hset("users", new_username, uid)

    print("Your personal data has been successfully updated!")
