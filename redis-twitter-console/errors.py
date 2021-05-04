"""This module is to catch custom operational errors."""


class DuplicateUserError(Exception):
    """Error will be thrown if there are duplicate users."""

    def __init__(self):
        super().__init__(self)
        self.message = "User is already registered!"


class EmptyInputError(Exception):
    """Error will be thrown if the user fails to enter an input."""

    def __init__(self):
        super().__init__(self)
        self.message = "Your input is empty! Please fill in the input!"


class FollowError(Exception):
    """Error will be thrown if the user attempts to follow themselves."""

    def __init__(self):
        super().__init__(self)
        self.message = "You cannot follow yourself!"


class NotAuthenticatedError(Exception):
    """Error will be thrown if the users is not authenticated."""

    def __init__(self):
        super().__init__(self)
        self.message = "You are not authenticated! Please log in!"


class UserDoesNotExistError(Exception):
    """Error will be thrown if the user searched does not exist."""

    def __init__(self):
        super().__init__(self)
        self.message = "User that you are looking for does not exist!"


class UserIsNotYourFollowingError(Exception):
    """Error will be thrown if the user is not a part of your 'following'."""

    def __init__(self):
        super().__init__(self)
        self.message = "User that you want to remove is not a part of your following!"
