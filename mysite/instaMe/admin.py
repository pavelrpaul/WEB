from django.contrib import admin

# Register your models here.
from instaMe.models import Comment
from instaMe.models import Photo, PLike

admin.site.register(Comment)
admin.site.register(Photo)
admin.site.register(PLike)