from django.db import models
from ultra_predictor.core.models import DefaultModel
from ultra_predictor.races.models import PredictionRace
from django.core.validators import MinValueValidator
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

    def save(self, *args, **kwargs):
        self.predicted = True
        self.prediction_time = datetime.timedelta(hours=10, minutes=20, seconds=59)
        super().save(*args, **kwargs)
