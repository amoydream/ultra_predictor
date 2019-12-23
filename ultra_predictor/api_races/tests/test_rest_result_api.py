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
    race = PredictionRaceFactory(itra_race_id=2)
    factory.force_authenticate(admin_user)
    request = factory.post(RACE_RESULTS_URL, race_result_payload)
    assert request.status_code == status.HTTP_201_CREATED
    
