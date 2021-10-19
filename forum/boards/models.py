from django.db import models
from django.db.models.fields import DateTimeField

from user.models import User

# Create your models here.
class Board(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=200) 
    user_create = models.ForeignKey(User, related_name='boards',  on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'board'

class Topic(models.Model):
    board = models.ForeignKey(Board, related_name='topics', on_delete=models.CASCADE)
    user_create = models.ForeignKey(User, related_name='topics',  on_delete=models.CASCADE)
    subject = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    #tags = models.CharField(max_length=150)

    class Meta:
        db_table = 'topic'
        unique_together = ('board', 'subject',)

class Post(models.Model):
    post_by = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, related_name='posts', on_delete=models.CASCADE)
    message = models.TextField(max_length=4000)
    creation_time = DateTimeField(auto_now_add=True)
    is_parent = models.BooleanField(default=False)

    class Meta:
        db_table = 'post'
        ordering = ['creation_time']


