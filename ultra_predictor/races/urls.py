from django.urls import path
from .views import PredictionRaceGroupListView, PredictionRaceResultGroupListView

app_name = "races"
urlpatterns = [
    path("", PredictionRaceGroupListView.as_view(), name="prediction-race-group-list"),
    path(
        "<uuid:pk>",
        PredictionRaceResultGroupListView.as_view(),
        name="prediction-group-detailed",
    ),
]
