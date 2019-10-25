from django.db import models
from ultra_predictor.core.models import DefaultModel
from django.core.validators import MinValueValidator


class PredictionRaceGroup(DefaultModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class PredictionRace(DefaultModel):
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
    name = models.CharField(max_length=256)
    start_date = models.DateField()
    distance = models.DecimalField(max_digits=6, decimal_places=2)
    prediction_race_group = models.ForeignKey(
        PredictionRaceGroup,
        on_delete=models.CASCADE,
        related_name="races",
        null=True,
        blank=True,
    )

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


class HistoricalRace(DefaultModel):
    FLAT = "f"
    MOUNTAIN = "m"
    RACE_TYPE_CHOICES = [(FLAT, "Flat"), (MOUNTAIN, "Mountain")]
    name = models.CharField(max_length=256)
    start_date = models.DateField()
    distance = models.DecimalField(max_digits=6, decimal_places=2)
    race_type = models.CharField(max_length=1, choices=RACE_TYPE_CHOICES, default="o")

    def __str__(self):
        return self.name


class Runner(DefaultModel):
    MAN = "m"
    WOMAN = "w"
    OTHER = "o"
    SEX_CHOICES = [(MAN, "Man"), (WOMAN, "Woman"), (OTHER, "Other")]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_year = models.IntegerField(validators=[MinValueValidator(1900)])
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, default="o")

    class Meta:
        unique_together = ["first_name", "last_name", "birth_year"]

    def __str__(self):
        return f"{self.name}, {self.birth_year}"

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"


class PredictionRaceResult(DefaultModel):
    runner = models.ForeignKey(
        Runner, on_delete=models.CASCADE, related_name="prediction_race_results"
    )
    time_result = models.DurationField()
    prediction_race = models.ForeignKey(
        PredictionRace, on_delete=models.CASCADE, related_name="prediction_race_results"
    )

    def __str__(self):
        return f"{self.runner.name}, {self.prediction_race.name}, {self.time_result}"


class HistoricalRaceResult(DefaultModel):
    runner = models.ForeignKey(
        Runner, on_delete=models.CASCADE, related_name="historical_race_results"
    )
    time_result = models.DurationField()
    historical_race = models.ForeignKey(
        HistoricalRace, on_delete=models.CASCADE, related_name="historical_race_results"
    )

    def __str__(self):
        return f"{self.runner.name}, {self.historical_race.name}, {self.time_result}"

