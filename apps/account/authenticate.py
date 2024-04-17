from apps.account.models import User


class EmailAuthBackend:
    """Custom authentication backend for authenticating users via email."""
    def authenticate(self, request, phone_number=None, password=None):  # noqa
        """
       Authenticate a user based on email and password.
       """
        try:
            user = User.objects.get(email=phone_number)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):  # noqa
        """
        Retrieve a user by user ID.

        Args:
            user_id (int): The ID of the user to retrieve.

        Returns:
            User: The user object if found, None otherwise.
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
