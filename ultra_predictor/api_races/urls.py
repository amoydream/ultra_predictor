from django.urls import path, include
from .api import EventAPI, RaceAPI, RaceResultAPI


app_name = "api_races"
urlpatterns = [
    path("api/events", EventAPI.as_view(), name="events"),
    path("api/races", RaceAPI.as_view(), name="races"),
    path("api/race_results", RaceResultAPI.as_view(), name="race_results"),
]

