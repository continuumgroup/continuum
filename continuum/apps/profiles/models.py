from django.contrib.auth.models import User
from django.db import models

from continuum.lib.choice import Choice

class RoleChoices(Choice):
    '''choices for UserProfile role'''
    CHARITY = 'charity'
    CLIENT = 'client'
    

class UserProfile(models.Model):
    '''extra information for user'''
    user = models.OneToOneField(User)
    role = models.CharField(
        max_length=RoleChoices.longest_length(),
        choices=RoleChoices, default=RoleChoices.CLIENT
    )

    def __unicode__(self):
        return u'Profile for %s' % self.user.username


def create_profile(sender, **kw):
    user = kw["instance"]
    if kw["created"]:
        UserProfile.objects.get_or_create(user=user)

models.signals.post_save.connect(create_profile, sender=User)
