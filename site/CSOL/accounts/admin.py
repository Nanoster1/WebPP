from django.contrib import admin
from .models import Profile, Friend


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo', 'site']


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Friend)
