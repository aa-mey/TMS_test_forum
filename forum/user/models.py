from django.db import models
from django.contrib.auth.models import User as auth_user
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, post_delete
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    # def user_dir_path(self, filename):
    #     print(filename, "\n\n\n")
    #     return 'user_{0}/{1}'.format(self.username, filename)

    username = models.CharField(max_length=200, unique=True)
    email = models.EmailField( unique=True)
    password = models.CharField(max_length=250)
    icon = models.ImageField(upload_to="user/", blank=True, null=True)

# @receiver(pre_save, sender=User)
# def hash_passwd(sender, instance, **kwargs):
#     instance.set_icon(instance.icon)

    # def save_user_profile(self, **kwargs):
    #     if self.id is None:
    #         saved_image = self.profile_image
    #         self.profile_image = None
    #         super(User, self).save(*args, **kwargs)
    #         self.profile_image = saved_image
    #         if 'force_insert' in kwargs:
    #             kwargs.pop('force_insert')
    #     super(User, self).save(*args, **kwargs)
        #instance.profile.save()
