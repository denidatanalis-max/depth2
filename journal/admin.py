from django.contrib import admin
from .models import UserProfile, Journal, JournalLog


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'manager']
    list_filter = ['role']
    search_fields = ['user__username', 'user__first_name', 'user__last_name']


@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'status', 'revision_count', 'updated_at']
    list_filter = ['status']
    search_fields = ['title', 'author__user__username']


@admin.register(JournalLog)
class JournalLogAdmin(admin.ModelAdmin):
    list_display = ['journal', 'action', 'by_user', 'timestamp']
    list_filter = ['action']
