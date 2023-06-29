from django.db import models
from .temple import temple
from .event import event
from django.contrib.auth.models import User

class post(models.Model):
  poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name='poster')
  username = models.CharField(max_length=200)
  title = models.CharField(max_length=200, default="new post")
  text = models.TextField()
  date_added = models.DateTimeField(auto_now_add=True)

class temple_post(post):
  temple = models.ForeignKey(temple, on_delete=models.CASCADE, related_name='posts')

class event_post(post):
  event = models.ForeignKey(event, on_delete=models.CASCADE, related_name='posts')

class comment(models.Model):
  commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commenter')
  username = models.CharField(max_length=200)
  text = models.TextField()
  parent_post = models.ForeignKey(post, on_delete=models.CASCADE, related_name='comment')
  date_added = models.DateTimeField(auto_now_add=True)


class commentReply(comment):
  parent_comment = models.ForeignKey(comment, on_delete=models.CASCADE, related_name='reply')