from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

class EventCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(EventCategory, on_delete=models.SET_NULL, null=True)
    short_description = models.CharField(max_length=300, blank=True)
    description = models.TextField()
    event_date = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    publish_date = models.DateTimeField(auto_now_add=True)
    location_name = models.CharField(max_length=255)
    address = models.TextField()
    map_embed_url = models.URLField(blank=True)
    featured_image = models.ImageField(upload_to='events/')
    event_video_url = models.URLField(blank=True)
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    attendance_count = models.PositiveIntegerField(default=0, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class RSVP(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='rsvps')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.event.title}"





