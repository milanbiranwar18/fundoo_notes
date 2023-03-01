from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    mob_num = models.IntegerField()
    location = models.CharField(max_length=100)
