from django.contrib import admin
from django.utils.html import format_html
from .models import PassRequest


@admin.register(PassRequest)
class PassRequestAdmin(admin.ModelAdmin):
    list_display = ['name', 'temple', 'visit_date', 'persons', 'status', 'created_at', 'action_buttons']
    list_filter = ['status', 'temple', 'visit_date']
    search_fields = ['name', 'email', 'phone']
    readonly_fields = ['created_at']

    def has_add_permission(self, request):
        return False

    def action_buttons(self, obj):
        if obj.status == 'PENDING':
            return format_html(
                '<button onclick="updateStatus({}, \'ACCEPTED\')" '
                'class="button button-accept">Accept</button> '
                '<button onclick="updateStatus({}, \'REJECTED\')" '
                'class="button button-reject">Reject</button>',
                obj.id, obj.id
            )
        return obj.get_status_display()

    action_buttons.short_description = 'Actions'