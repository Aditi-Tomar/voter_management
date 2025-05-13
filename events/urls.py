from django.urls import path, include
from .views import RSVPCreateAPIView, UpcomingEventsAPIView, PastEventsAPIView, EventsByCategoryAPIView
from . import views

urlpatterns = [
    path('preview/int:pk/', views.event_detail_view, name='event-preview'),
    path('archive/int:pk/', views.ArchiveEventAPIView.as_view(), name='event-archive'),
    path('api/preview/int:pk/', views.EventPreviewAPIView.as_view(), name='api-event-preview'),
    path('api/upcoming/', views.UpcomingEventsAPIView.as_view(), name='api-upcoming-events'),
    path('api/past/', views.PastEventsAPIView.as_view(), name='api-past-events'),
    path('api/category/int:category_id/', views.EventsByCategoryAPIView.as_view(), name='api-category-events'),
    path('api/rsvp/', views.RSVPCreateAPIView.as_view(), name='api-rsvp'),
]