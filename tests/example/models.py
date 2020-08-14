from rested import models
from rested.middleware.token import TokenUserMixin
from django.contrib.auth.models import AbstractUser

class Person(models.Model):
    name = models.TextField()
    avatar = models.FileField()

class User(AbstractUser, TokenUserMixin):
    token = models.CharField(max_length=128, null=True)
