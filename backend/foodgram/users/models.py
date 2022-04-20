from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.db import models


class User(AbstractUser):
    """Модель User."""
    email = models.EmailField(
        verbose_name='Почта',
        max_length=36,
        validators=[validators.validate_email],
        unique=True,
        blank=False
        )

    is_staff = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)

    # Свойство `USERNAME_FIELD` сообщает нам, какое поле мы будем использовать
    # для входа.
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ('username',)

    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        blank=False
    )

    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        blank=False
    )
