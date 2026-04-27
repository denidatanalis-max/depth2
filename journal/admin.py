from django.contrib import admin
from .models import UserProfile, Journal, JournalLog, JournalScore


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'manager']
    list_filter = ['role']
    search_fields = ['user__username', 'user__first_name', 'user__last_name']


@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'status', 'revision_count', 'published_at', 'updated_at']
    list_filter = ['status']
    search_fields = ['title', 'author__user__username']


@admin.register(JournalScore)
class JournalScoreAdmin(admin.ModelAdmin):
    list_display = ['journal', 'scorer', 'total_score', 'recommendation', 'created_at']
    list_filter = ['recommendation']


@admin.register(JournalLog)
class JournalLogAdmin(admin.ModelAdmin):
    list_display = ['journal', 'action', 'by_user', 'timestamp']
    list_filter = ['action']
