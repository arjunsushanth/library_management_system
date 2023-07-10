from django.db import models
from django.contrib.auth.models import AbstractUser






class User(AbstractUser):


    USER_TYPE = [
    ('member', 'MEMBER'),
    ('librarian', 'LIBRARIAN'),
    ]

    user_type = models.CharField(choices=USER_TYPE,max_length=250,)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    












   