from django.db import models
from django.contrib.auth.models import User

from Divinearme.search.models.temples import temple

class event(models.Model):
    religious_establishment = models.ForeignKey(temple, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    date = models.DateField()
    invited_users = models.ManyToManyField(User, through='invitation')
    # Additional fields for the event

    def __str__(self):
        return self.name