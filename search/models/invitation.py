from django.db import models
from django.contrib.auth.models import User
from .user_profile import UserModel
from .temple import temple
from .event import event

class invitation(models.Model):
    is_accepted = models.BooleanField(default=False)
    # Additional fields for the invitation
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')])
    invite_time = models.DateTimeField(auto_now_add=True)

    # Additional fields for the invitation, such as a message or date
    
class TempleInvitation(invitation):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="temple_invitations")
    associated_temple = models.ForeignKey(temple, on_delete=models.CASCADE, related_name="invited_users_invitations")

    #class Meta:
        #constraints = [models.UniqueConstraint(fields=['associated_temple', 'user'], name='unique-temple-invitation')]

    def accept_invitation(self):
        self.status = 'accepted'
        self.associated_temple.temple_members.add(self.user)
        self.associated_temple.save()
        self.save()
    
    def reject_invitation(self):
        self.status = 'rejected'
        self.save()
    
    def __str__(self):
        return f"Invitation: {self.user.user.username} - {self.associated_temple.name}"

class EventInvitation(invitation):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="event_invitations")
    associated_event = models.ForeignKey(event, on_delete=models.CASCADE, related_name="invited_users_invitations")
    
    #class Meta:
        #constraints = [models.UniqueConstraint(fields=['associated_event', 'user'], name='unique-event-invitation')]
    def accept_invitation(self):
        self.status = 'accepted'
        self.is_accepted = True
        self.associated_event.event_members.add(self.user)
        self.associated_event.save()
        self.save()
    
    def reject_invitation(self):
        self.is_accepted = False
        self.status = 'rejected'
        self.save()
    
    def __str__(self):
        return f"Invitation: {self.user.user.username} - {self.associated_event.name}"