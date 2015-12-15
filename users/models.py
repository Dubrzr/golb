from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, **user_data):
        user = self.model()
        print(dict(user_data))
        user.set_password(user_data.pop('password'))
        for key, value in user_data.items():
            setattr(user, key, value)
        user.save(using=self.db)
        return user

    def create_superuser(self, **user_data):
        user = self.create_user(**user_data)
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self.db)
        return user


class User(AbstractBaseUser):
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'is_admin']

    first_name = models.CharField(max_length=254)
    last_name = models.CharField(max_length=254)
    username = models.CharField(max_length=254, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    date_joined = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.is_superuser = self.is_admin
            self.is_staff = self.is_admin
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)
