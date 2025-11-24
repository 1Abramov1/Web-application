from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Кастомная модель пользователя с дополнительными полями.
    Наследуется от AbstractUser для расширения стандартной модели.
    """
    # Переопределяем поле username, чтобы использовать email для авторизации
    username = None

    # Поле для авторизации - email
    email = models.EmailField(
        unique=True,
        verbose_name='Электронная почта'
    )

    # Дополнительные поля
    avatar = models.ImageField(
        upload_to='users/avatars/',
        blank=True,
        null=True,
        verbose_name='Аватар',
        help_text='Загрузите ваш аватар'
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Номер телефона',
        help_text='Введите номер телефона'
    )

    country = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Страна',
        help_text='Введите вашу страну'
    )

    # Явно переопределяем поля groups и user_permissions с кастомными related_name
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="custom_user_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="custom_user_set",
        related_query_name="user",
    )

    # Указываем поле для аутентификации
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['email']

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        """
        Возвращает полное имя пользователя.
        """
        return f"{self.first_name} {self.last_name}".strip()
