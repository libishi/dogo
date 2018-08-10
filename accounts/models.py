from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dog = models.BooleanField(default=True)
    cat = models.BooleanField(default=True)
    bird = models.BooleanField(default=True)
    kennel = models.TextField(max_length=500, blank=True)
    breed = models.TextField(max_length=100, blank=True)
    age = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)

    def get_connections(self):
        connections = Connection.objects.filter(creator=self.user)
        return connections

    def get_followers(self):
        followers = Connection.objects.filter(following=self.user)
        return followers

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Connection(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    creator = models.ForeignKey(User, related_name="friendship_creator_set")
    following = models.ForeignKey(User, related_name="friend_set")
