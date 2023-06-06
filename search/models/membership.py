from django.db import models
from django.contrib.auth.models import User

from Divinearme.search.models.temples import temple


class membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    religious_establishment = models.ForeignKey(temple, on_delete=models.CASCADE)
    joined_date = models.DateField(auto_now_add=True)
    # Additional fields for the membership

    def __str__(self):
        return f"{self.user.username} - {self.religious_establishment.name}"
