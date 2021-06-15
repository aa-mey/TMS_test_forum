from django.db import models
from django.contrib.auth.models import User as auth_user
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser

def user_dir_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class User(AbstractUser):
    username = models.CharField(max_length=200, unique=True)
    email = models.EmailField(max_length=200, unique=True)
    password = models.CharField(max_length=250)
    icon = models.FileField(upload_to=user_dir_path, blank=True)

    @receiver(post_save, sender=auth_user)
    def create_user(sender, instance, created, **kwargs):
        if created:
            auth_user.objects.create(username=instance)

    @receiver(post_save, sender=auth_user)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
