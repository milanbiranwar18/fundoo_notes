from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    mob_num = models.IntegerField()
    location = models.CharField(max_length=100)


class UserLog(models.Model):
    method = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
