from rest_framework import serializers
from ultra_predictor.races.models import Event, PredictionRace


class PredictionRaceSerilazer(serializers.ModelSerializer):
    class Meta:
        model = PredictionRace
        fields = [
            "id",
            "name",
            "start_date",
            "distance",
            "elevation_gain",
            "elevation_lost",
            "itra",
            "food_point",
            "time_limit",
        ]


class EventSerializer(serializers.ModelSerializer):
    races = PredictionRaceSerilazer(
        many=True, read_only=True, source="prediction_races"
    )

    class Meta:
        model = Event
        fields = ["id", "name", "start_date", "end_date", "races"]

