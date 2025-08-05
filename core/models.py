from django.db import models
from django.conf import settings
from tinymce.models import HTMLField
from django.utils.text import slugify


class SupportPreference(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='support_preference')
    preference = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)  # When first created
    updated_at = models.DateTimeField(auto_now=True)  # When last modified

    def __str__(self):
        return f"{self.user.email} - {self.preference}"

    class Meta:
        verbose_name = "Support Preference"
        verbose_name_plural = "Support Preferences"
        ordering = ['-updated_at']
        db_table = 'tbl_support_preferences'


class Event(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"
        ordering = ['-created_at']
        db_table = 'tbl_events'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ContactMessage(models.Model):
    support_option = models.CharField(max_length=100)
    subject = models.CharField(max_length=255)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tbl_contact_messages'
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.subject} by {self.name}"


class Appointment(models.Model):
    APPOINTMENT_WITH_CHOICES = [
        ('doctor', 'Doctor'),
        ('pharmacist', 'Pharmacist'),
        ('assistant', 'Pharmacy Assistant'),
    ]
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    appointment_with = models.CharField(max_length=20, choices=APPOINTMENT_WITH_CHOICES)
    appointment_datetime = models.DateTimeField()

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.appointment_with}"


class Pages(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = HTMLField()

    def __str__(self):
        return self.title


class FAQ(models.Model):
    page = models.ForeignKey(Pages, on_delete=models.CASCADE, related_name='faqs')
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return self.question