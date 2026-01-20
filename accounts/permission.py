from django.contrib.auth.models import AbstractBaseUser

def is_admin(user: AbstractBaseUser) -> bool:
    """
    Check whether the given user has administrative access.

    Args:
        user (AbstractBaseUser): The user instance to check.

    Returns:
        bool: True if the user is authenticated and is a staff user,
              False otherwise.
    """
    return user.is_authenticated and user.is_staff

