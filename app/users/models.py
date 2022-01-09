import datetime

from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, \
    AbstractUser
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from django.conf import settings


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        """Creates and returns a new user with Token"""
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        username = extra_fields.get('username')
        user.username = username if username else user.email
        user.set_password(password)
        user.is_active = False
        user.save(using=self._db)
        Token.objects.create(user=user)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """Creates and returns a new superuser with Token"""
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        Token.objects.create(user=user)
        return user


class User(AbstractUser):
    """Custom user model with unique username and email"""
    email = models.EmailField(max_length=64, unique=True,)
    first_name = models.CharField(max_length=64, blank=True)
    last_name = models.CharField(max_length=64, blank=True)
    username = models.CharField(max_length=64, unique=True, blank=True)
    age = models.PositiveIntegerField(null=True)
    activation_key = models.CharField(max_length=128, null=True, blank=True)
    activation_key_expiration_date = models.DateTimeField(null=True, blank=True)

    objects = UserManager()

    # EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    # TODO
    def set_activation_key(self):
        pass

    # TODO
    def activation_key_is_valid(self):
        return True if self.activation_key_expiration_date > datetime.datetime.now() else False

    # TODO
    def activate(self):
        self.is_active = True
        self.save()


    # @receiver(models.signals.post_save, sender=settings.AUTH_USER_MODEL)
    # def create_auth_token(sender, instance, created, **kwargs):
    #     if created:
    #         Token.objects.create(user=instance)
