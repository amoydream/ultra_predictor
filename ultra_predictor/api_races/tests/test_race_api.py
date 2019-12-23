from django.test import TestCase
from django.urls import reverse
import os

from unittest.mock import patch


from rest_framework.test import APIClient
from rest_framework import status
from ultra_predictor.races.tests.factories import EventFactory
from ultra_predictor.races.models import PredictionRace
RACE_URL = reverse("api_races:races")


def test_create_race(admin_user, race_payload):
    """ Only staff can add Events"""
    factory = APIClient()
    event = EventFactory(itra_id=1000, year=2018)
    race_payload['itra_event_id'] = 1000
    race_payload['itra_race_id'] = 1
    race_payload['race_date'] = f"{event.year}-12-08"
    factory.force_authenticate(admin_user)
    request = factory.post(RACE_URL, race_payload)
    added_race = PredictionRace.objects.last()
    assert request.status_code == status.HTTP_201_CREATED
    assert added_race.event == event