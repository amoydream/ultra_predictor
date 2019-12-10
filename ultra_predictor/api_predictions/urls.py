from django.urls import path, include

from .api import PredictionAPI

app_name = "api_predictions"
urlpatterns = [path("api/predictions", PredictionAPI.as_view(), name="predict")]
