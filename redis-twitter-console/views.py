"""This module is to store our views, or print statements."""

import sys

from os import system


def exit_menu() -> None:
    """Exits the program."""
    print("Thanks for using this Redis playground!")
    sys.exit()


def main_menu() -> None:
    """This view is to render our simple main menu."""
    system("cls")
    print("======================================")
    print("         Redis Python Example         ")
    print("======================================")
    print("1. Sign Up")
    print("2. Log In")
    print("3. Get My Profile")
    print("4. Tweet")
    print("5. Follow Someone")
    print("6. Search Profile")
    print("7. Unfollow Someone")
    print("8. Timeline")
    print("9. Update Username")
    print("10. Logout")
    print("11. Exit")
    print("12. Get All Data (Debug)")
    print("13. Flush Database (Debug)")
