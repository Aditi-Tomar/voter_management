from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework import generics, permissions, filters
from django.utils.timezone import now
from .models import Event, EventCategory, RSVP
from .serializers import EventSerializer, EventCategorySerializer, RSVPSerializer
from django.shortcuts import get_object_or_404, render

def event_detail_view(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'events/event_detail.html', {'event': event})

class RSVPCreateAPIView(generics.CreateAPIView):
    queryset = RSVP.objects.all()
    serializer_class = RSVPSerializer
    permission_classes = [permissions.AllowAny]

class UpcomingEventsAPIView(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Event.objects.filter(event_date__gte=now(), is_published=True, is_archived=False).order_by(
            'event_date')
        is_featured = self.request.query_params.get('is_featured')
        category_id = self.request.query_params.get('category')
        if is_featured:
            queryset = queryset.filter(is_featured=is_featured.lower() == 'true')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset

class PastEventsAPIView(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Event.objects.filter(event_date__lt=now(), is_published=True).order_by('-event_date')

class EventsByCategoryAPIView(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        category_id = self.kwargs.get("category_id")
        return Event.objects.filter(category_id=category_id, is_published=True).order_by('-event_date')

class EventPreviewAPIView(APIView):
    def get(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)

class ArchiveEventAPIView(APIView):
    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        event.is_archived = True
        event.save()
        return Response({'status': 'archived'}, status=status.HTTP_200_OK)

    def event_detail_view(request, pk):
        event = get_object_or_404(Event, pk=pk)
        return render(request, 'events/event_detail.html', {'event': event})

