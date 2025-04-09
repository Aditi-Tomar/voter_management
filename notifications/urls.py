from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('api/templates/', views.get_all_templates, name='all-templates'),
    path('get_templates/<int:type_id>/', views.get_templates, name='get_templates'),
    path('api/send/', views.send_notifications, name='send-notifications'),
]
