import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

client = APIClient(HTTP_HOST='localhost')


@pytest.mark.django_db
def test_user_signup(payload_fixture):
    payload_fixture['password2'] = payload_fixture['password']
    response = client.post(reverse('signup'), payload_fixture)
    data = response.data

    assert data['first_name'] == payload_fixture['first_name']
    assert data['last_name'] == payload_fixture['last_name']
    assert data['email'] == payload_fixture['email']
    assert payload_fixture['password'] not in data.values()
    assert payload_fixture['password2'] not in data.values()

    del payload_fixture['password2']


@pytest.mark.django_db
def test_user_login(correct_user_fixture, payload_fixture):
    response = client.post(reverse('token_obtain_pair'), dict(
        email=correct_user_fixture.email,
        password=payload_fixture['password']
    ))
    data = response.data

    assert data['access']
    assert data['refresh']


@pytest.mark.django_db
def test_user_login_fail(wrong_user_fixture, payload_fixture):
    response = client.post(reverse('token_obtain_pair'), dict(
        email=wrong_user_fixture.email,
        password=payload_fixture['password']
    ))
    assert response.status_code == 401


@pytest.mark.django_db
def test_user_logout(correct_user_fixture):
    refresh = RefreshToken.for_user(correct_user_fixture)
    response = client.post(
        reverse('logout'),
        {'refresh': str(refresh)},
        HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}'
    )
    assert response.status_code == 204
