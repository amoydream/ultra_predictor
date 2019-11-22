from django.contrib.auth import get_user_model
from django.urls import reverse


from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse("api_account:register")


def test_create_user_api_endpoint(db):
    factory = APIClient()
    request = factory.post(
        CREATE_USER_URL,
        {"username": "john", "email": "test@mojek.pl", "password": "django123456"},
    )
    
    assert request.status_code, status.HTTP_201_CREATED
