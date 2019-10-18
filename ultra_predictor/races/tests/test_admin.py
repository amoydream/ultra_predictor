from django.urls import reverse
from .factories import RaceFactory
from ultra_predictor.users.tests.factories import UserFactory
import pytest


@pytest.fixture
def login_admin_user(db, client):
    admin_user = UserFactory(is_superuser=True, is_active=True, is_staff=True)
    client.force_login(admin_user)
    return admin_user


@pytest.fixture
def race(db):
    return RaceFactory()


def test_listing_races(login_admin_user, race, client):
    """Test simple listening races"""
    url = reverse("admin:races_race_changelist")
    res = client.get(url)
    assert str(race) in str(res.content)


def test_make_race_ready_custom_action(login_admin_user, client, race):
    """Test that race can change status from unready to ready"""
    url = reverse("admin:races_race_changelist")
    data = {"action": "make_race_ready", "_selected_action": [race.id]}
    res = client.post(url, data)
    race.refresh_from_db()
    assert race.itra_download_status == 'R'
