from django.contrib import admin
from app.models import UserProfile, UserCard


class UserProfileAdmin(admin.ModelAdmin):
    pass

class UserCardAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserCard, UserCardAdmin)