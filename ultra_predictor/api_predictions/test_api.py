from django.test import TestCase
from django.urls import reverse


# Create your tests here.
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from ultra_predictor.races.tests.factories import PredictionRaceFactory

PREDICTION_URL = reverse("api_predictions:predict")


def pred_payload(race, best_ten="00:50:00", sex="m", birth_year=1980):
    payload = {
        "race": race,
        "best_ten": best_ten,
        "sex": sex,
        "birth_year": birth_year,
    }
    return payload


def test_prediction_endpoint_without_user_logedin(db):
    race = PredictionRaceFactory()
    payload = pred_payload(race=race.id)
    factory = APIClient()
    request = factory.post(PREDICTION_URL, payload)
    assert request.status_code == status.HTTP_401_UNAUTHORIZED

def test_prediction_endpoint_with_login_user(db):
    race = PredictionRaceFactory()
    payload = pred_payload(race=race.id)
    user = get_user_model().objects.create_user("test@mojek.pl", "pass123")
    factory = APIClient()
    factory.force_authenticate(user)
    request = factory.post(PREDICTION_URL, payload)
    
    assert request.status_code == status.HTTP_201_CREATED



