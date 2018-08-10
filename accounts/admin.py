from django.contrib import admin

# Register your models here.
from .models import UserProfile, Connection


class UserProfileModelAdmin(admin.ModelAdmin):
    list_display = ["user"]

    class Meta:
        model = UserProfile


class ConnectionModelAdmin(admin.ModelAdmin):
    list_display = ["created"]

    class Meta:
        model = Connection


admin.site.register(UserProfile, UserProfileModelAdmin)
admin.site.register(Connection, ConnectionModelAdmin)
