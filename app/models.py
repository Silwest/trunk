from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save


class UserProfile(models.Model):
    user = models.ForeignKey(User)

    class Meta:
        def __init__(self):
            pass

        ordering = ['-id']

    def __unicode__(self):
        return ("{0} - {1} {2}".format(self.user.username, self.user.first_name, self.user.last_name))


def create_user_profile(sender, instance, **kwargs):
    if not UserProfile.objects.filter(user=instance):
        profile = UserProfile.objects.create(user=instance)
        profile.save()


post_save.connect(create_user_profile, sender=User, dispatch_uid='my_unique_identifier')