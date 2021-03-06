import pandas as pd
from django.test import TestCase
from ultra_predictor.race_predictions.extras.prediction_data_preparation import (
    PredictionDataPreparation,
)


class TestPredictor(TestCase):
    def test_init(self):
        predictor = PredictionDataPreparation(
            best_ten_run_in_hours=1.3,
            sex="M",
            month="April",
            runner_age=30,
            itra_point=3,
            refreshment_points=3,
            max_time=10.3,
            ascent=1000,
            descent=1000,
        )
        assert isinstance(predictor, PredictionDataPreparation)
        assert isinstance(predictor.to_dataframe(), pd.DataFrame)
        df = predictor.to_dataframe()

        assert df["ascent"][0] == predictor.ascent
        assert df["April"][0] == 1
        assert df["January"][0] == 0
