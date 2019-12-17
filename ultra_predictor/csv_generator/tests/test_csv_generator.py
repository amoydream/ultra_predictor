from django.test import TestCase
import os
import pytest
from ultra_predictor.races.models import PredictionRaceGroup, PredictionRaceResult
from ultra_predictor.csv_generator.extras.csv_generator import CsvGenerator
from ultra_predictor.races.tests.factories import (
    PredictionRaceGroupFactory,
    PredictionRaceFactory,
    RunnerFactory,
    PredictionRaceResultFactory,
    HistoricalRaceFactory,
    HistoricalRaceResultFactory,
)
import shutil
from django.conf import settings


@pytest.mark.slow
class TestCsvCreator(TestCase):
    def setUp(self):
        for _ in range(0, 10):
            group = PredictionRaceGroupFactory()
            for _ in range(0, 10):
                race1 = PredictionRaceFactory(prediction_race_group=group)
                for _ in range(0, 10):
                    result = PredictionRaceResultFactory(prediction_race=race1)
                    historical_race = HistoricalRaceFactory(distance=10)
                    HistoricalRaceResultFactory(
                        runner=result.runner, historical_race=historical_race
                    )

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(settings.PREDICTION_ML_FOLDER)

    def test_csv_creation_init(self):
        group = PredictionRaceGroup.objects.first()
        csv_gen = CsvGenerator(group=group)
        csv_file = csv_gen.csv_file
        assert csv_file.endswith(".csv")

    def test_csv_creation_file_name(self):
        group = PredictionRaceGroup.objects.first()
        csv_gen = CsvGenerator(group=group)
        csv_file = csv_gen.csv_file
        assert (
            csv_file
            == f"{settings.CSV_FILE_PREDICTION_GROUP_NAME_TEMPLATE}{group.id}.csv"
        )

    def test_csv_count_line_nubers_of_file(self):
        group = PredictionRaceGroup.objects.first()
        number_of_results = group.all_results_of_prediction_races().count()
        csv_gen = CsvGenerator(group=group)
        assert number_of_results == csv_gen.rows_number()  # plus 1 for column names

    def test_csv_without_group(self):
        number_of_results = PredictionRaceResult.objects.count()
        csv_gen = CsvGenerator()
        assert number_of_results == csv_gen.rows_number()  # plus 1 for column names
