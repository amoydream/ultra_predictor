from rest_framework import serializers

from django.contrib.auth import get_user_model, authenticate
from ultra_predictor.races.models import PredictionRace
from ultra_predictor.race_predictions.models import RacePrediction


class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RacePrediction
        fields = [
            "id",
            "race",
            "user",
            "sex",
            "birth_year",
            "best_ten",
            "predicted",
            "prediction_time",
        ]
        read_only_fields = ["id", "user" ,"prediction_time", "predicted"]
        

