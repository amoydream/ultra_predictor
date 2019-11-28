from .serializers import EventSerializer
from rest_framework import generics, permissions
from ultra_predictor.races.models import Event

from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class EventAPI(generics.ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    queryset = Event.objects.all()
    serializer_class = EventSerializer
