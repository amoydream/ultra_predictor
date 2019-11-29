from .serializers import EventSerializer
from rest_framework import generics, permissions
from ultra_predictor.races.models import Event





class EventAPI(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    queryset = Event.objects.all()
    serializer_class = EventSerializer
