from django.db import models
from django.contrib.auth.models import User


class user_profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()
    location = models.CharField(max_length=200)
    # Additional fields for the user profile

    def __str__(self):
        return self.user.username