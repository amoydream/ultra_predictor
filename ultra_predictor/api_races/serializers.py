import logging
from rest_framework import serializers
from django.db import transaction
import datetime
from ultra_predictor.races.models import (
    Event,
    PredictionRace,
    PredictionRaceResult,
    Runner,
)

logger = logging.getLogger(__name__)


class PredictionRaceResultSerilazer(serializers.Serializer):
    first_name = serializers.CharField(max_length=256, required=True)
    last_name = serializers.CharField(max_length=256, required=True)
    time_result = serializers.DurationField(required=False)
    position = serializers.IntegerField(required=False)
    sex = serializers.CharField(max_length=1, required=True)
    nationality = serializers.CharField(max_length=256)
    birth_year = serializers.IntegerField(required=True)
    itra_race_id = serializers.IntegerField(required=True)
    itra_race_year = serializers.IntegerField(required=True)
    itra_runner_id = serializers.IntegerField(required=True)

    

    def create(self, validated_data):
        with transaction.atomic():
            prediction_race = PredictionRace.objects.get(
                itra_race_id=validated_data["itra_race_id"],
                race_date__year=validated_data["itra_race_year"],
            )
            runner, runner_created = Runner.objects.get_or_create(
                first_name=validated_data["first_name"],
                last_name=validated_data["last_name"],
                sex=validated_data["sex"],
                nationality=validated_data["nationality"],
                birth_year=validated_data["birth_year"],
                itra_runner_id=validated_data["itra_runner_id"],
            )

            result, result_created = PredictionRaceResult.objects.get_or_create(
                runner=runner,
                prediction_race=prediction_race,
                time_result=validated_data.get("time_result"),
                position=validated_data.get("position"),
            )
            logger.info(
                "{} Runner: {}".format(
                    "Added:" if runner_created else "already exists:", runner
                )
            )
            logger.info(
                "{} PredictionRaceResult: {}".format(
                    "Added:" if result_created else "already exists:", result
                )
            )

        return validated_data


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

