from decimal import Decimal
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from ultra_predictor.races import models


@registry.register_document
class RaceResult(Document):
    best_ten_run_in_hours = fields.DoubleField()
    time_result_in_hours = fields.DoubleField(attr="time_result_in_hours")
    runner_age = fields.IntegerField(attr="runner_age_during_race")
    itra_point = fields.IntegerField()

    def prepare_itra_point(self, instance):
        return instance.prediction_race.itra

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

        fields = ["position"]

