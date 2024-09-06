from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Chat(models.Model):
    message = models.TextField()
    response = models.TextField()

    def __str__(self):
        return f'{self.message}'