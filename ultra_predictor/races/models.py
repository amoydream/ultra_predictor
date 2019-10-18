from django.db import models
from ultra_predictor.core.models import DefaultModel
from django.core.validators import MinValueValidator


class RaceGroup(DefaultModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Race(DefaultModel):
    UNREADY = "U"
    READY = "R"
    STARTED = "S"
    COMPLETED = "C"
    FAILURE = "F"
    ITRA_DOWNLOAD_STATUSES = (
        (UNREADY, "Unready"),
        (READY, "Ready"),
        (STARTED, "Started"),
        (COMPLETED, "Completed"),
        (FAILURE, "Failure"),
    )
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
    itra_download_status = models.CharField(
        max_length=1, choices=ITRA_DOWNLOAD_STATUSES, default=UNREADY
    )

    def __str__(self):
        return self.name

class Runner(DefaultModel):
    name = models.CharField(max_length=100)
    birth_year = models.IntegerField(validators=[MinValueValidator(1900)])

    class Meta:
        unique_together = ["name", "birth_year"]

    def __str__(self):
        return f"{self.name}, {self.birth_year}"
