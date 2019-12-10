from .serializers import EventSerializer
from rest_framework import generics, permissions
from ultra_predictor.races.models import Event
#import time


class EventAPI(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
