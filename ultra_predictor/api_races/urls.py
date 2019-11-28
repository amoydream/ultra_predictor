from django.urls import path, include
from .api import EventAPI


app_name = "api_races"
urlpatterns = [path("api/events", EventAPI.as_view(), name="events")]

