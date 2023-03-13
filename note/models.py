from django.db import models

# Create your models here.
from user.models import User


class Labels(models.Model):
    label_name = models.CharField(max_length=150, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Note(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    label = models.ManyToManyField(Labels)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=1500)
    collaborator = models.ManyToManyField(User, related_name='collaborator')
    isArchive = models.BooleanField(default=False)
    isTrash = models.BooleanField(default=False)
    color = models.CharField(max_length=10, null=True, blank=True)
    reminder = models.DateTimeField(null=True, blank=True)
    image = models.ImageField(upload_to='notes_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)







