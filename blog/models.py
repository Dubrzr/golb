from datetime import datetime
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, name, email, password=None):
        user = self.model(name=name, email=email)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, name, email, password):
        user = self.create_user(name=name, email=email)
        user.set_password(password)
        user.is_admin = True
        user.save(using=self.db)
        return user

class User(AbstractBaseUser):
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    first_name = models.CharField(max_length=254)
    last_name = models.CharField(max_length=254)
    username = models.CharField('user name', max_length=254, unique=True)
    email = models.EmailField('email address', max_length=254, unique=True)
    date_joined = models.DateTimeField(default=datetime.now)
    is_admin = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)
            # Do more things here
        else:
            super().save(*args, **kwargs)
