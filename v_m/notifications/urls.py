from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('api/templates/<int:type_id>/', views.get_templates, name='get-templates'),
    path('api/send/', views.send_notifications, name='send-notifications'),
]