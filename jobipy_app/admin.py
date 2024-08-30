from django.contrib import admin
from .models import User, Job_Post, Preferences

# Register your models here.
admin.site.register(User)
admin.site.register(Job_Post)
admin.site.register(Preferences)
