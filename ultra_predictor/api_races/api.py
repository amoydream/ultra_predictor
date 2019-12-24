from .serializers import (
    EventSerializer,
    PredictionRaceSerilazer,
    PredictionRaceResultSerilazer,
)
from rest_framework import generics, permissions
from ultra_predictor.races.models import (
    Event,
    PredictionRace,
    PredictionRaceResult,
    Runner,
)
from rest_framework.response import Response
import logging

logger = logging.getLogger(__name__)
# import time


class CreateOnlyAdminUser(permissions.IsAuthenticated):
    def has_permission(self, request, view):

        if request.method == "POST" and not request.user.is_staff:
            return False
        return super().has_permission(request, view)


class EventAPI(generics.ListCreateAPIView):
    permission_classes = (CreateOnlyAdminUser,)
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class RaceAPI(generics.ListCreateAPIView):
    permission_classes = (CreateOnlyAdminUser,)
    queryset = PredictionRace.objects.all()
    serializer_class = PredictionRaceSerilazer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def perform_create(self, serializer):
        try:

            year_of_event = self.request.data["race_date"].split("-")[0]
            event = Event.objects.get(
                itra_id=self.request.data["itra_event_id"], year=year_of_event
            )
            serializer.save(event=event)
        except Event.DoesNotExist:
            logger.error(f"Event not found: {self.request.data}")


class RaceResultAPI(generics.ListCreateAPIView):
    permission_classes = (CreateOnlyAdminUser,)
    queryset = PredictionRaceResult.objects.all()
    serializer_class = PredictionRaceResultSerilazer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        
        serializer = PredictionRaceResultSerilazer(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=201)

