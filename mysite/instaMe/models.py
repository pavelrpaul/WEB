from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    # filename = models.CharField(max_length=50, default='default.png')
    filename = models.ImageField(upload_to='/uploads/', default='default.png')

    def __unicode__(self):
        return str(self.user.username)
# class Photo(models.Model):
# 	filename = 

class PLike(models.Model):
	author = models.ForeignKey(User)
	value = models.IntegerField(default=0)

class Photo(models.Model):
	filename = models.ImageField(upload_to='/uploads/', default='default.png')
	likes = models.ManyToManyField(PLike)
	data = models.DateTimeField(default=datetime.now)
	author = models.ForeignKey(User)

	def __unicode__(self):
		return str(self.title)

class Comment(models.Model):
	text = models.TextField()
	data = models.DateTimeField(default=datetime.now)
	author = models.ForeignKey(User)
	photo = models.ForeignKey(Photo)

	def __unicode__(self):
		return str(self.title)


