from django.db import models
from django.contrib.auth.models import User

from .temple import temple
from .event import event

class invitation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)
    # Additional fields for the invitation
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')])

    # Additional fields for the invitation, such as a message or date

    def accept_invitation(self):
        self.status = 'accepted'

    def reject_invitation(self):
        self.status = 'rejected'
    
class temple_invitation(invitation):
    associated_temple = models.ForeignKey(temple, on_delete=models.CASCADE)

    def accept_invitation(self):
        self.status = 'accepted'
        self.associated_temple.temple_members.add(self.user)
        self.associated_temple.save()
        self.save()
    
    def reject_invitation(self):
        self.status = 'rejected'
        self.save()
    
    def __str__(self):
        return f"Invitation: {self.user.username} - {self.associated_temple.name}"

class event_invitation(invitation):
    associated_event = models.ForeignKey(event, on_delete=models.CASCADE)
    
    def accept_invitation(self):
        self.status = 'accepted'
        self.associated_event.event_members.add(self.user)
        self.associated_event.save()
        self.save()
    
    def reject_invitation(self):
        self.status = 'rejected'
        self.save()
    
    def __str__(self):
        return f"Invitation: {self.user.username} - {self.associated_event.name}"

class temple_request(temple_invitation):
    pass
class event_request(event_invitation):
    pass