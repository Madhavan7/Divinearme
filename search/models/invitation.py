from django.db import models
from django.contrib.auth.models import User

from Divinearme.search.models.temples import temple
from Divinearme.search.models.event import event

class Invitation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    associated_event = models.ForeignKey(event, on_delete=models.CASCADE)
    invited_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invitations_sent')
    is_accepted = models.BooleanField(default=False)
    # Additional fields for the invitation

    def __str__(self):
        return f"Invitation: {self.user.username} - {self.event.name}"