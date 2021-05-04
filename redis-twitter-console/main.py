"""This module is the starting point of our application."""

from typing import Union

# Our modules
from authentication import sign_in, sign_up, with_authentication
from database import redis_init, get_all_data, flush_database
from errors import (
    DuplicateUserError,
    EmptyInputError,
    FollowError,
    NotAuthenticatedError,
    UserDoesNotExistError,
    UserIsNotYourFollowingError,
)
from users import (
    follow,
    logout,
    profile,
    other_profile,
    timeline,
    tweet,
    unfollow,
    update_profile,
)
from views import exit_menu, main_menu


def main():
    """Main function that will be run in the application."""
    # Only needs this global variable to keep track of sessions
    authentication: Union[int, bool] = False

    # Initialize redis
    redis = redis_init()

    # Enter infinite loop
    while True:
        main_menu()

        try:
            choice = int(input("Input: "))

            if choice == 1:
                sign_up(redis)

            elif choice == 2:
                authentication = sign_in(redis)

            elif choice == 3:
                with_authentication(profile, authentication, redis, authentication)

            elif choice == 4:
                with_authentication(tweet, authentication, redis, authentication)

            elif choice == 5:
                with_authentication(follow, authentication, redis, authentication)

            elif choice == 6:
                with_authentication(other_profile, authentication, redis)

            elif choice == 7:
                with_authentication(unfollow, authentication, redis, authentication)

            elif choice == 8:
                timeline(redis)

            elif choice == 9:
                with_authentication(
                    update_profile, authentication, redis, authentication
                )

            elif choice == 10:
                authentication = logout()

            elif choice == 11:
                exit_menu()

            elif choice == 12:
                get_all_data(redis)

            elif choice == 13:
                flush_database(redis)

            else:
                raise ValueError()

        except ValueError:
            print("Please input a correct value!")
            continue

        except (
            DuplicateUserError,
            EmptyInputError,
            FollowError,
            NotAuthenticatedError,
            UserDoesNotExistError,
            UserIsNotYourFollowingError,
        ) as err:
            print(err.message)
            continue

        finally:
            input("\nPress any key to continue!")


if __name__ == "__main__":
    main()
