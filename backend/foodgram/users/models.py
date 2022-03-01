from django.contrib.auth.models import AbstractUser
from django.db import models


class Roles(models.Model):
    USER = 'user'
    ADMIN = 'admin'
    ROLE_CHOICES = (
        (ADMIN, 'Администратор'),
        (USER, 'Аутентифицированный пользователь'),
    )


class User(AbstractUser):
    email = models.EmailField(
        verbose_name='Почта',
        max_length=36,
    )

    username = models.CharField(
        verbose_name='Логин',
        max_length=24,
        unique=True,
    )

    first_name = models.CharField(
        verbose_name='Имя',
        max_length=24,
    )

    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=24,
    )

    password = models.CharField(
        verbose_name='Пароль',
        max_length=24,
    )

    role = models.CharField(
        verbose_name='Роль',
        max_length=50,
        choices=Roles.ROLE_CHOICES,
        default='user'
    )
