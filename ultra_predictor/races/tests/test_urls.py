import pytest
from django.conf import settings
from django.urls import reverse, resolve
from .factories import PredictionRaceGroupFactory, PredictionRaceFactory

pytestmark = pytest.mark.django_db


def test_race_group_list_urls(client, admin_user):
    client.force_login(admin_user)
    response = client.get(reverse("races:prediction-race-group-list"))
    assert "predictionracegroup_list.html" in [t.name for t in response.templates]
    assert response.status_code == 200


def test_race_group_list_urls(client, admin_user):
    client.force_login(admin_user)
    group1 = PredictionRaceGroupFactory(name="Wielka Prehyba")
    group2 = PredictionRaceGroupFactory(name="Maraton Bieszczadzki 52km")
    response = client.get(reverse("races:prediction-race-group-list"))
    assert "<h1>Races</h1>" in str(response.content)
    assert group1.name in str(response.content)
    assert group2.name in str(response.content)


def test_races_below_race_group_urls(client, admin_user):
    client.force_login(admin_user)
    race = PredictionRaceFactory(name="Wielka Prehyba 2019")
    group = race.prediction_race_group
    response = client.get(reverse("races:prediction-race-group-list"))
    assert group.name in str(response.content)
    assert race.name in str(response.content)


def test_url_for_all_result_for_a_group(client, admin_user):
    client.force_login(admin_user)
    group1 = PredictionRaceGroupFactory(name="Wielka Prehyba")
    response = client.get(reverse("races:prediction-group-detailed", args=[group1.pk]))
    assert response.status_code == 200

