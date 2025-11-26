from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


class EmailBackend(ModelBackend):
    """
    Кастомный бэкенд для аутентификации по email
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        # Используем email вместо username
        email = kwargs.get('email', username)
        if email is None:
            email = username

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None