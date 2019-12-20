from django.test import TestCase
from django.urls import reverse
import os

from unittest.mock import patch


from rest_framework.test import APIClient
from rest_framework import status
from ultra_predictor.races.tests.factories import EventFactory

EVENTS_URL = reverse("api_races:events")


def test_create_event_logged_out(db, event_payload):
    event = EventFactory()
    factory = APIClient()
    request = factory.post(EVENTS_URL, event_payload)
    assert request.status_code == status.HTTP_401_UNAUTHORIZED

def test_create_event_logged_in_as_normal_user(db, current_user, event_payload):
    event = EventFactory()
    factory = APIClient()
    factory.force_authenticate(current_user)
    request = factory.post(EVENTS_URL, event_payload)
    assert request.status_code == status.HTTP_403_FORBIDDEN

def test_create_event_logged_in_as_admin_user(admin_user, event_payload):
    """ Only staff can add Events"""
    event = EventFactory()
    factory = APIClient()
    factory.force_authenticate(admin_user)
    request = factory.post(EVENTS_URL, event_payload)
    assert request.status_code == status.HTTP_201_CREATED

def test_create_event_with_the_same_event(admin_user, event_payload):
    """ Only staff can add Events"""
    event = EventFactory()
    factory = APIClient()
    factory.force_authenticate(admin_user)
    request = factory.post(EVENTS_URL, event_payload)
    request = factory.post(EVENTS_URL, event_payload)
    assert request.status_code == status.HTTP_400_BAD_REQUEST

def test_create_event_with_the_same_event(admin_user, event_payload):
    """ Only staff can add Events"""
    event = EventFactory()
    factory = APIClient()
    factory.force_authenticate(admin_user)
    request = factory.post(EVENTS_URL, event_payload)
    request = factory.post(EVENTS_URL, event_payload)
    assert request.status_code == status.HTTP_400_BAD_REQUEST



# def test_create_event_logged_In(db, event_payload):
#     event = EventFactory()
#     factory = APIClient()
#     user = get_user_model().objects.create_user("test@mojek.pl", "pass123")
#     factory = APIClient()
#     factory.force_authenticate(user)
#     request = factory.post(EVENTS_URL, event_payload)
#     assert request.status_code == status.HTTP_401_UNAUTHORIZED