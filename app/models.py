import random
from ubuntuone.syncdaemon.tritcask import timestamp
import datetime
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save


class UserCard(models.Model):
    cardNumber = models.IntegerField(max_length=9, unique=True, blank=False, null=False)
    created = models.DateField(blank=True, null=True)
    validTo = models.DateField(blank=True, null=True)


    class Meta:
        ordering = ['-id']

    def __unicode__(self):
        return unicode(self.cardNumber)


    def save(self, *args, **kwargs):
        ''' On save, update created and validTo fields
        '''

        if not self.id:
            self.cardNumber = random.randint(1, 999999999)
            print datetime.date.today()
            self.created = datetime.date.today()
            self.validTo = datetime.date.today() + datetime.timedelta(days=30)  # valid for 30 days
        super(UserCard, self).save(*args, **kwargs)


class UserProfile(models.Model):
    user = models.ForeignKey(User, help_text='Database user')
    userCard = models.ForeignKey(UserCard, blank=True, null=True,
                                   help_text="Numer karty identyfikacyjnej.")
    class Meta:
        def __init__(self):
            pass

        ordering = ['-id']

    def __unicode__(self):
        return ("{0} - {1} {2}".format(self.user.username, self.user.first_name, self.user.last_name))

    def save(self, *args, **kwargs):
        if not self.id:
            self.userCard = UserCard.objects.create()
        return super(UserProfile, self).save(*args, **kwargs)


def create_user_profile(sender, instance, **kwargs):
    if not UserProfile.objects.filter(user=instance):
        profile = UserProfile.objects.create(user=instance)


post_save.connect(create_user_profile, sender=User, dispatch_uid='my_unique_identifier')