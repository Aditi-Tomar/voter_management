from django.contrib import admin
from django.template.response import TemplateResponse
from django.urls import path
from django.http import JsonResponse
from django.utils.html import format_html
import json
from .models import Voter, VoterField
from notifications.models import NotificationType, NotificationTemplate
from rangefilter.filters import DateRangeFilter


@admin.register(Voter)
class VoterAdmin(admin.ModelAdmin):
    change_list_template = 'admin/voters/voter/change_list.html'
    list_per_page = 50
    actions = ['send_notification']

    def get_list_display(self, request):
        """Dynamically generate list_display based on VoterFields"""
        try:
            fields = VoterField.objects.all()
            if not fields.exists():
                return ['id', 'get_data', 'created_at', 'updated_at']

            custom_fields = ['get_' + field.name for field in fields]
            return ['id'] + custom_fields + ['created_at', 'updated_at']
        except:
            return ['id', 'get_data', 'created_at', 'updated_at']

    def get_data(self, obj):
        """Display JSON data in a readable format"""
        return format_html(
            '<pre style="max-width: 500px; white-space: pre-wrap;">{}</pre>',
            json.dumps(obj.data, indent=2)
        )

    get_data.short_description = 'Data'

    def get_queryset(self, request):
        """Add custom filtering"""
        queryset = super().get_queryset(request)

        # Handle custom filters from GET parameters
        filters = {}
        for key, value in request.GET.items():
            if key.startswith('filter_') and value:
                field_name = key[7:]  # Remove 'filter_' prefix
                filters[f'data__{field_name}__icontains'] = value

        if filters:
            queryset = queryset.filter(**filters)

        return queryset

    def changelist_view(self, request, extra_context=None):
        """Add extra context for the template"""
        extra_context = extra_context or {}
        extra_context.update({
            'voter_fields': VoterField.objects.all(),
            'notification_types': NotificationType.objects.all(),
        })
        return super().changelist_view(request, extra_context=extra_context)

    def get_urls(self):
        """Add custom URLs for AJAX operations"""
        urls = super().get_urls()
        custom_urls = [
            path(
                'get-templates/<int:type_id>/',
                self.admin_site.admin_view(self.get_templates),
                name='get-templates'
            ),
            path(
                'send/',
                self.admin_site.admin_view(self.send_notifications),
                name='send-notifications'
            ),
        ]
        return custom_urls + urls

    def get_templates(self, request, type_id):
        """AJAX endpoint to get templates for a notification type"""
        templates = NotificationTemplate.objects.filter(notification_type_id=type_id)
        return JsonResponse({
            'templates': [{'id': t.id, 'name': t.name} for t in templates]
        })

    def send_notifications(self, request):
        """AJAX endpoint to send notifications"""
        if request.method != 'POST':
            return JsonResponse({'success': False, 'error': 'Invalid request method'})

        try:
            selected_voters = json.loads(request.POST.get('selected_voters', '[]'))
            notification_type = request.POST.get('notification_type')
            template_id = request.POST.get('notification_template')
            channel = request.POST.get('notification_channel')

            if not all([selected_voters, notification_type, template_id, channel]):
                return JsonResponse({
                    'success': False,
                    'error': 'Missing required parameters'
                })

            # Get the template
            template = NotificationTemplate.objects.get(id=template_id)

            # Get the selected voters
            voters = Voter.objects.filter(id__in=selected_voters)

            # Create notification logs and send notifications
            from notifications.utils import NotificationSender
            sender = NotificationSender()

            for voter in voters:
                phone = voter.data.get('phone')
                if not phone:
                    continue

                # Send notification based on channel
                if channel in ['SMS', 'BOTH']:
                    sender.send_sms(phone, template.content)
                if channel in ['WA', 'BOTH']:
                    sender.send_whatsapp(phone, template.content)

            return JsonResponse({'success': True})

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        # Dynamically add methods for each field
        try:
            fields = VoterField.objects.all()
            for field in fields:
                method_name = f'get_{field.name}'
                if not hasattr(self, method_name):
                    setattr(
                        self,
                        method_name,
                        lambda obj, field_name=field.name: obj.data.get(field_name, '')
                    )
                    # Set short description for the column
                    getattr(self, method_name).short_description = field.name
        except:
            pass


@admin.register(VoterField)
class VoterFieldAdmin(admin.ModelAdmin):
    list_display = ('name', 'field_type', 'is_required')
    search_fields = ('name',)