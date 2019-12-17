from django.db import models
from ultra_predictor.core.models import DefaultModel
from ultra_predictor.races.models import PredictionRace
from django.core.validators import MinValueValidator
from ultra_predictor.race_predictions.extras.prediction_data_preparation import (
    PredictionDataPreparation,
)
from ultra_predictor.race_predictions.extras.linear_predictor import LinearPredictor

import datetime

# Create your models here.
from django.conf import settings


class RacePrediction(DefaultModel):
    MAN = "m"
    WOMAN = "w"
    OTHER = "o"
    SEX_CHOICES = [(MAN, "Man"), (WOMAN, "Woman"), (OTHER, "Other")]

    race = models.ForeignKey(
        PredictionRace, on_delete=models.CASCADE, related_name="prediction_races"
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, default="o")
    birth_year = models.PositiveSmallIntegerField(validators=[MinValueValidator(1900)])
    best_ten = models.DurationField()
    predicted = models.BooleanField(default=False)
    prediction_time = models.DurationField(null=True, blank=True)

    @property
    def runner_age_during_race(self):
        return self.race.start_date.year - self.birth_year

    def save(self, *args, **kwargs):
        self.predicted = True
        hours = self.prepare_prediction()
        self.prediction_time = datetime.timedelta(hours=hours)
        super().save(*args, **kwargs)

    def prepare_prediction(self):
        prediction_data = PredictionDataPreparation(
            best_ten_run_in_hours=self.best_ten.seconds / 3600,
            sex=self.sex,
            month=self.race.month_of_the_race,
            distance=self.race.distance,
            runner_age=self.runner_age_during_race,
            itra_point=self.race.itra,
            food_point=self.race.food_point,
            time_limit=self.race.time_limit,
            elevation_gain=self.race.elevation_gain,
            elevation_lost=self.race.elevation_lost,
        )
        predictor = LinearPredictor()
        result = predictor.prediction(prediction_data)
        return result
