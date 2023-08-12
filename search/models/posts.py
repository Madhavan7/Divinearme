from django.db import models

from search.models.user_profile import UserModel
from .temple import temple
from .event import event
from .user_profile import UserModel
from django.contrib.auth.models import User

class post(models.Model):
  poster = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='poster')
  username = models.CharField(max_length=200)
  title = models.CharField(max_length=200, default="new post")
  text = models.TextField()
  date_added = models.DateTimeField(auto_now_add=True)

  def can_view(viewer: UserModel):
    raise NotImplementedError

  def can_delete(self, viewer:UserModel):
    return (viewer.id == self.poster)
  
class TemplePost(post):
  templeID = models.ForeignKey(temple, on_delete=models.CASCADE, related_name='posts')

  def can_view(self, viewer: UserModel):
    return temple.objects.get(id = self.templeID).temple_members.filter(id = viewer.id).exists()
  
  def can_delete(self, viewer:UserModel):
    return super().can_delete() or temple.objects.get(id = self.templeID).admins.filter(id = viewer.id).exists()

class EventPost(post):
  eventID = models.ForeignKey(event, on_delete=models.CASCADE, related_name='posts')

  def can_view(self, viewer: UserModel):
    return event.objects.get(id = self.eventID).event_members.filter(id = viewer.id).exists()
  
  def can_delete(self, viewer:UserModel):
    even = event.objects.get(id = self.eventID)
    temp = temple.objects.get(id = even.associated_temple)
    return super().can_delete() or temp.admins.filter(id = viewer.id).exists()

class comment(models.Model):
  commenter = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='commenter')
  username = models.CharField(max_length=200)
  text = models.TextField()
  parent_post = models.ForeignKey(post, on_delete=models.CASCADE, related_name='comment')
  date_added = models.DateTimeField(auto_now_add=True)


class CommentReply(comment):
  parent_comment = models.ForeignKey(comment, on_delete=models.CASCADE, related_name='reply')