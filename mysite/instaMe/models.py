from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    # filename = models.CharField(max_length=50, default='default.png')
    filename = models.ImageField(upload_to='/uploads/', default='default.png')

    def __unicode__(self):
        return str(self.user.username)