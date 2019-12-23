from rest_framework import serializers
from ultra_predictor.races.models import Event, PredictionRace, PredictionRaceResult

class PredictionRaceResultSerilazer(serializers.ModelSerializer):
    class Meta:
        model = PredictionRaceResult
        fields = [
            
            "time_result",
            "position",
            "prediction_race"
        ]
class PredictionRaceSerilazer(serializers.ModelSerializer):
    class Meta:
        model = PredictionRace
        fields = [
            "id",
            "name",
            "itra_event_id",
            "itra_race_id",
            "itra_race_event_id",
            "itra_point",
            "mount_point",
            "finish_point",
            "map_link",
            "participation",
            "sentiers",
            "pistes",
            "routes",
            "challenge",
            "championship",
            "country_start",
            "city_start",
            "country_finish",
            "city_finish",
            "distance",
            "race_date",
            "race_time",
            "ascent",
            "descent",
            "refreshment_points",
            "max_time",
        ]


class EventSerializer(serializers.ModelSerializer):
    races = PredictionRaceSerilazer(
        many=True, read_only=True, source="prediction_races"
    )

    class Meta:
        model = Event
        fields = ["id", "name", "year", "itra_id", "races"]

