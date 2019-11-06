from django.urls import path
from . import views

app_name = "races"
urlpatterns = [
    path("", views.PredictionRaceGroupListView.as_view(), name="prediction-race-group-list"),
    path(
        "<uuid:pk>",
        views.PredictionRaceResultGroupListView.as_view(),
        name="prediction-group-detailed",
    ),
    
]
