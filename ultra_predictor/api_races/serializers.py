from rest_framework import serializers
from ultra_predictor.races.models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["name", "start_date", "end_date", "prediction_races"]
