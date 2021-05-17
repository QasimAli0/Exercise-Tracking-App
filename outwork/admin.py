from django.contrib import admin
from .models import UserData, Workout, Follows
# Register your models here.

admin.site.register(UserData)
admin.site.register(Workout)
admin.site.register(Follows)
