from email.policy import default
from typing import List
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    username = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=127, unique=True)
    birthdate = models.DateField()
    bio = models.TextField(blank=True, null=True)
    is_critic = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    REQUIRED_FIELDS: List[str] = [
        'email',
        'first_name', 'last_name', 'birthdate'
    ]
