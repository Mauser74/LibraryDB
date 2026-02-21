from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Пользователь должен иметь e-mail')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)



class CustomUser(AbstractUser):
    # username = None
    username = models.CharField(
        max_length=100,
        unique=False,
        null=False,
        blank=False,
        verbose_name='Имя пользователя'
    )

    email = models.EmailField(
        max_length=255,
        unique=True,
        verbose_name='E-mail пользователя'
    )

    date_of_birth = models.DateField(
        blank=False,
        null=False,
        verbose_name='Дата рождения'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'date_of_birth']

    objects = CustomUserManager()

    def __str__(self):
        return self.username






