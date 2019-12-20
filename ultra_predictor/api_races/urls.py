from django.urls import path, include
from .api import EventAPI, RaceAPI


app_name = "api_races"
urlpatterns = [
    path("api/events", EventAPI.as_view(), name="events"),
    path("api/races", RaceAPI.as_view(), name="races"),
]

