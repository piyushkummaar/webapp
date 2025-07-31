from django.contrib import admin
from core.models import SupportPreference, Event, ContactMessage


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at', 'updated_at')
    search_fields = ('name', 'slug')
    prepopulated_fields = {"slug": ("name",)}
    ordering = ('-created_at',)


@admin.register(SupportPreference)
class SupportPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'preference', 'created_at', 'updated_at')
    search_fields = ('user__email', 'preference')
    list_filter = ('preference', 'created_at')
    ordering = ('-updated_at',)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'support_option', 'submitted_at')
    search_fields = ('name', 'email', 'subject', 'message')
    list_filter = ('support_option', 'submitted_at')
    ordering = ('-submitted_at',)
