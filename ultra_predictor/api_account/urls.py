from django.urls import path, include
from .api import RegisterAPI, LoginAPI
from knox import views as knox_views

app_name = "api_account"
urlpatterns = [
    path("api/auth", include("knox.urls")),
    path("api/auth/register", RegisterAPI.as_view(),  name="register"),
    path("api/auth/login", LoginAPI.as_view(),  name="login"),
]

