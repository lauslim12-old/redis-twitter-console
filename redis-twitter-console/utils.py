"""This module is to store our utilities."""


def is_string_blank(string: str) -> bool:
    """Checks if a string is empty/blank or not.

    Parameters:
    ----------
    string (str): String to be checked.

    Returns:
    -------
    bool: Bool value whether the string is empty or not.
    """
    if string and string.strip():
        return False

    return True
