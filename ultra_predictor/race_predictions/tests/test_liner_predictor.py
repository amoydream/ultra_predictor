import os
import pandas as pd
from django.test import TestCase
from ultra_predictor.race_predictions.extras.linear_predictor import LinearPredictor
from ultra_predictor.race_predictions.extras.prediction_data_preparation import (
    PredictionDataPreparation,
)

from unittest.mock import patch

CURRENT_APP_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TestLinearPredictor(TestCase):
    def setUp(self):
        self.file_path = CURRENT_APP_PATH + "/tests/fixtures/prediction_all.csv"

    def test_init(self):
        predictor = LinearPredictor()
        assert not predictor.model_is_ready

    @patch(
        "ultra_predictor.race_predictions.extras.linear_predictor.LinearPredictor.load_file"
    )
    def test_create_model(self, load_file):
        load_file.return_value = self.file_path
        predictor = LinearPredictor()
        predictor.create_model()
        assert predictor.model_is_ready

    @patch(
        "ultra_predictor.race_predictions.extras.linear_predictor.LinearPredictor.load_file"
    )
    def test_load_model(self, load_file):
        load_file.return_value = self.file_path
        predictor = LinearPredictor()
        predictor.create_model()
        predictor.load_model()
        assert predictor.model

    @patch(
        "ultra_predictor.race_predictions.extras.linear_predictor.LinearPredictor.load_file"
    )
    def test_prediction(self, load_file):
        prediction_data = PredictionDataPreparation(
            best_ten_run_in_hours=0.9,
            sex="M",
            month="December",
            distance=64.1,
            runner_age=38,
            itra_point=2,
            refreshment_points=4,
            max_time=14,
            ascent=2740,
            descent=2590,
        )
        load_file.return_value = self.file_path
        predictor = LinearPredictor()
        # predictor.create_model()
        # predictor.load_model()
        result = predictor.prediction(prediction_data)
        assert isinstance(result, float)

