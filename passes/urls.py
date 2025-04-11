from django.urls import path
from . import views
from . import api

app_name = 'passes'

urlpatterns = [
    path('request/', views.request_pass, name='request_pass'),
    path('api/submit/', api.submit_pass_request, name='submit_pass_request'),
    path('api/<int:request_id>/update-status/', api.update_request_status, name='update_request_status'),

]