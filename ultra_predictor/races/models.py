from django.db import models
from ultra_predictor.core.models import DefaultModel


class RaceGroup(DefaultModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Race(DefaultModel):
    race_group = models.ForeignKey(
        RaceGroup, on_delete=models.CASCADE, related_name="races", null=True, blank=True
    )
    name = models.CharField(max_length=256)
    start_date = models.DateField()
    distance = models.DecimalField(max_digits=6, decimal_places=2)
    elevation_gain = models.PositiveIntegerField()
    elevation_lost = models.PositiveIntegerField()
    itra = models.PositiveIntegerField()
    itra_race_id = models.PositiveIntegerField()
    food_point = models.PositiveIntegerField()
    time_limit = models.DecimalField(max_digits=10, decimal_places=1)

    def __str__(self):
        return self.name

