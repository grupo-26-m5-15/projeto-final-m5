from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.CharField(max_length=150, unique=True)
    birthdate = models.DateField(null=True)
    cpf = models.CharField(max_length=11, unique=True)
    image = models.URLField(null=True)
    is_superuser = models.BooleanField(default=False, null=True)
