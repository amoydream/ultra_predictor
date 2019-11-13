from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from ultra_predictor.races import models


@registry.register_document
class RaceResult(Document):
    class Index:
        name = "race_results"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = models.PredictionRaceResult
        best_ten_run = fields.TextField(attr="best_10km_run_before_prediction_race")
        fields = ["position"]

