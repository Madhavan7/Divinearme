from django.db import models
from django.contrib.auth.models import User

class UserModel(models.Model):
    private = models.BooleanField(default=False)
    user = models.OneToOneField(User, related_name='model', on_delete=models.CASCADE)
    biography = models.TextField(blank=True)
    class Meta:
        ordering = ["user__username"]
    def __str__(self):
        return self.user.username