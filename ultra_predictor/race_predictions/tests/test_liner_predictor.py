# import os
# from django.test import TestCase
# from ultra_predictor.race_predictions.extras.linear_predictor import LinearPredictor

# CURRENT_APP_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# class TestLinearPredictor(TestCase):
#     def setUp(self):
#         with open(CURRENT_APP_PATH + "/tests/fixtures/prediction_all.csv") as f:
#             self.csv = f.read()

#     def test_init(self):
#         predictor = LinearPredictor()
#         assert not predictor.model_is_ready

#     def test_create_model(self):
#         predictor = LinearPredictor()
#         predictor.create_model()
#         assert predictor.model_is_ready
