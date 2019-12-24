from django.test import TestCase
from django.urls import reverse
import os

from unittest.mock import patch


from rest_framework.test import APIClient
from rest_framework import status
from ultra_predictor.races.tests.factories import EventFactory, PredictionRaceFactory
from ultra_predictor.races.models import PredictionRace

RACE_RESULTS_URL = reverse("api_races:race_results")


def test_create_race_results(admin_user, race_result_payload):
    """ Only staff can add Events"""
    factory = APIClient()
    race = PredictionRaceFactory(
        itra_race_id=race_result_payload['itra_race_id'],
        race_date=f"{race_result_payload['itra_race_year']}-12-08")
    factory.force_authenticate(admin_user)
    request = factory.post(RACE_RESULTS_URL, race_result_payload)
    assert request.status_code == status.HTTP_201_CREATED
    assert race.runners.count() == 1
    assert race.prediction_race_results.count() == 1

def test_create_race_result_with_dnf(admin_user, race_result_payload):
    """ Only staff can add Events"""
    race_result_payload['position'] = ''
    race_result_payload['time_result'] = ''
    factory = APIClient()
    race = PredictionRaceFactory(
        itra_race_id=race_result_payload['itra_race_id'],
        race_date=f"{race_result_payload['itra_race_year']}-12-08")
    factory.force_authenticate(admin_user)
    request = factory.post(RACE_RESULTS_URL, race_result_payload)
    assert request.status_code == status.HTTP_201_CREATED
    assert race.runners.count() == 1
    assert race.prediction_race_results.count() == 1
    assert race.prediction_race_results.first().position == None
    assert race.prediction_race_results.first().time_result == None

