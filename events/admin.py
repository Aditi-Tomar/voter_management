from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_featured', 'is_published', 'actions')

    def actions(self, obj):
        return format_html(
            '<a class="button" href="{}">Preview</a>&nbsp;'
            '<a class="button" href="{}">Edit</a>&nbsp;'
            '<a class="button" href="{}">{}</a>',
            reverse('admin:event_event_preview', args=[obj.pk]),
            reverse('admin:event_event_change', args=[obj.pk]),
            reverse('admin:event_event_archive', args=[obj.pk]),
            'Unarchive' if obj.is_archived else 'Archive'
        )
    actions.short_description = 'Actions'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if 'archived' in request.GET:
            return qs.filter(is_archived=True)
        return qs

    def archive_event(self, request, queryset):
        queryset.update(is_archived=True)
    archive_event.short_description = "Archive selected events"

    def unarchive_event(self, request, queryset):
        queryset.update(is_archived=False)
    unarchive_event.short_description = "Unarchive selected events"

    actions = ['archive_event', 'unarchive_event']