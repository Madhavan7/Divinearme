from django.db import models
from django.contrib.auth.models import User

class user_model(models.Model):
    user = models.OneToOneField(User, related_name='model', on_delete=models.CASCADE)
    biography = models.TextField(blank=True)
    def __str__(self):
        return self.user.username