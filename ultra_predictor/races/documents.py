from decimal import Decimal
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from ultra_predictor.races import models


@registry.register_document
class RaceResult(Document):
    # runner info
    runner_age = fields.IntegerField(attr="runner_age_during_race")
    best_ten_run_in_hours = fields.DoubleField()
    runner_sex = fields.StringField(attr="runner.sex")
    # race info
    itra_point = fields.IntegerField(attr="prediction_race.itra")
    food_point = fields.IntegerField(attr="prediction_race.food_point")
    time_limit = fields.IntegerField(attr="prediction_race.time_limit")
    month_of_the_race = fields.StringField(attr="prediction_race.month_of_the_race")
    distance = fields.StringField(attr="prediction_race.distance")
    elevation_gain = fields.StringField(attr="prediction_race.elevation_gain")
    elevation_lost = fields.StringField(attr="prediction_race.elevation_lost")
    # result info
    time_result_in_hours = fields.DoubleField(attr="time_result_in_hours")
    position = fields.IntegerField(attr="position")

    def prepare_best_ten_run_in_hours(self, instance):
        if instance.best_10km_run_before_prediction_race:
            hours = Decimal(
                instance.best_10km_run_before_prediction_race.seconds / 3600
            )
            return round(hours, 2)
        else:
            return None

    class Index:
        name = "race_results"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = models.PredictionRaceResult


