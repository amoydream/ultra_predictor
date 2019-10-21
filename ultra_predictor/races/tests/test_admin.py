from django.urls import reverse
from .factories import PredictionRaceFactory
from ultra_predictor.users.tests.factories import UserFactory
import pytest


@pytest.fixture
def login_admin_user(db, client):
    admin_user = UserFactory(is_superuser=True, is_active=True, is_staff=True)
    client.force_login(admin_user)
    return admin_user


@pytest.fixture
def prediction_race(db):
    return PredictionRaceFactory()


def test_listing_races(login_admin_user, prediction_race, client):
    """Test simple listening races"""
    url = reverse("admin:races_predictionrace_changelist")
    res = client.get(url)
    assert str(prediction_race) in str(res.content)


def test_make_race_ready_custom_action(login_admin_user, client, prediction_race):
    """Test that race can change status from unready to ready"""
    url = reverse("admin:races_predictionrace_changelist")
    data = {"action": "make_race_ready", "_selected_action": [prediction_race.id]}
    res = client.post(url, data)
    prediction_race.refresh_from_db()
    assert prediction_race.itra_download_status == 'R'
