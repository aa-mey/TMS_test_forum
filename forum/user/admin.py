from django.contrib import admin
from user.models import User

class AdminUser(admin.ModelAdmin):
    list_display = ["username", "email", "icon"]

admin.site.register(User, AdminUser)
