from django.db import models
from django.contrib.auth.models import User

from Divinearme.search.models.temple import temple
from Divinearme.search.models.event import event

class invitation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    associated_event = models.ForeignKey(event, on_delete=models.CASCADE)
    invited_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invitations_sent')
    is_accepted = models.BooleanField(default=False)
    # Additional fields for the invitation
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')])

    # Additional fields for the invitation, such as a message or date

    def accept_invitation(self):
        self.status = 'accepted'
        self.event.invited_users.add(self.user)
        self.event.save()
        self.save()

    def reject_invitation(self):
        self.status = 'rejected'
        self.save()

    def __str__(self):
        return f"Invitation: {self.user.username} - {self.event.name}"