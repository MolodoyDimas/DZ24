from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


from django.contrib.auth.models import BaseUserManager

# ответ из интернета, так как не создавался суперпользователь с ошибкой:
# TypeError: UserManager.create_superuser() missing 1 required positional argument: 'username'
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class UserRoles(models.TextChoices):
    MEMBER = 'member', _('member')
    MODERATOR = 'moderator', _('moderator')


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, max_length=150, verbose_name='Почта')
    phone = models.IntegerField(verbose_name='Телефон', blank=True, null=True)
    avatar = models.ImageField(upload_to='user/', verbose_name='Аватар', blank=True, null=True)
    city = models.CharField(max_length=150, verbose_name='Город', blank=True, null=True)
    role = models.CharField(max_length=9, choices=UserRoles.choices, default=UserRoles.MEMBER)

    last_login = models.DateTimeField(auto_now=True, verbose_name='Последний вход', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()