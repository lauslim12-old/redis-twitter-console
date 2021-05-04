"""This Python module is for authentication purposes."""

from time import time
from typing import Callable, Literal, Union

from redis import Redis

from errors import DuplicateUserError, EmptyInputError, NotAuthenticatedError
from utils import is_string_blank


def auth_guard(uid: int) -> bool:
    """Checks if the current user is authenticated or not.

    Parameters:
    -----------
    uid (int): User id

    Returns:
    --------
    bool: If the user is logged is logged in, else raise exception
    """
    if not uid:
        raise NotAuthenticatedError()

    return True


def sign_in(redis: Redis) -> Union[int, bool]:
    """Logs in a user with an algorithm.

    Algorithm:
    ----------
    1. Get username and password.
    2. Sanity check, ensure that inputs are fulfilled.
    3. Check if username exists. If yes, fetch data from 'user' HSET.
    4. Check if passwords match.

    Parameters:
    -----------
    redis (Redis): Redis instance

    Returns:
    --------
    int or None: Either integer or boolean
    """
    username = input("Input your username: ")
    password = input("Input your password: ")

    if is_string_blank(username) or is_string_blank(password):
        raise EmptyInputError()

    user_id = redis.hget("users", username)

    if not user_id:
        print("Wrong username or password!")
        return False

    real_password = redis.hget(f"user:{user_id}", "password")

    if password != real_password:
        print("Wrong username or password!")
        return False

    print("You have been successfully authenticated!")
    return user_id


def sign_up(redis: Redis):
    """Signs up a user. Algorithm:

    Algorithm:
    ----------
    1. Increment 'user_id'.
    2. Sanity check, if username or password is empty, raise exception.
    3. Check if the user exists.
    4. Store username and password in a 'user' HSET.
    5. Store the primary key (user_id) in 'users' HSET for easy fetching.

    Parameters:
    -----------
    redis (Redis): Redis instance

    Returns:
    --------
    None

    """
    username = input("Input your username: ")
    password = input("Input your password: ")

    if is_string_blank(username) or is_string_blank(password):
        raise EmptyInputError()

    if redis.hexists("users", username):
        raise DuplicateUserError()

    user_id = redis.incr("next_user_id")

    user_data = {
        "uid": user_id,
        "username": username,
        "password": password,
        "registration_date": int(time()),
        "modification_date": int(time()),
    }

    redis.hset(f"user:{user_id}", mapping=user_data)
    redis.hset("users", username, user_id)

    print("You have been successfully signed up!")


def with_authentication(
    custom_function: Callable, uid: int, *args: tuple
) -> Union[Callable, bool]:
    """Closure that returns a function, used to check for authentication."""
    if auth_guard(uid):
        return custom_function(*args)

    return False
