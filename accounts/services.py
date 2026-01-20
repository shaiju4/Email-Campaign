from django.contrib.auth.models import User


def create_user(username: str, password: str) -> User:
    """
    Create a new user with the given username and password.

    Args:
        username (str): The username for the new user.
        password (str): The password for the new user.

    Returns:
        User: The newly created  User instance.
    """
    user = User.objects.create_user(
        username=username,
        password=password
    )
    return user
