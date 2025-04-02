from django.urls import path
from . import views

app_name = 'voters'

urlpatterns = [
    path('list/', views.voter_list, name='voter-list'),
]