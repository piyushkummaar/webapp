from django.contrib import admin
from core.models import (
    SupportPreference,
    Event,
    ContactMessage,
    Pages,
    FAQ,
    Appointment)


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


class FAQInline(admin.TabularInline):
    model = FAQ
    extra = 1


@admin.register(Pages)
class PagesAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [FAQInline]


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'page')
    search_fields = ('question', 'answer')


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'appointment_with', 'appointment_datetime', 'email', 'phone')
    list_filter = ('appointment_with', 'appointment_datetime')
    search_fields = ('first_name', 'last_name', 'email', 'phone')
