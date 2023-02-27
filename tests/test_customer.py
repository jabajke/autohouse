import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

client = APIClient(HTTP_HOST='localhost')


@pytest.mark.django_db
def test_create_correct_offer(
        customer_fixture,
        logged_in_user,
        prefer_car_correct_fixture
):
    payload = dict(
        preferred_car=prefer_car_correct_fixture,
        price=100,
    )
    response = client.post(
        reverse('offer-list'),
        payload,
        format='json',
        HTTP_AUTHORIZATION=f'Bearer {logged_in_user.get("access")}'
    )
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_create_offer_with_invalid_price(
        customer_fixture,
        logged_in_user,
        prefer_car_correct_fixture
):
    customer_fixture.balance = 0
    customer_fixture.save()
    payload = dict(
        preferred_car=prefer_car_correct_fixture,
        price=1000
    )
    response = client.post(
        reverse('offer-list'),
        payload,
        format='json',
        HTTP_AUTHORIZATION=f'Bearer {logged_in_user.get("access")}'
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_get_offer(
        logged_in_user,
        offer_fixture
):
    response = client.get(
        reverse('offer-detail', kwargs={"pk": offer_fixture.pk}),
        HTTP_AUTHORIZATION=f'Bearer {logged_in_user.get("access")}'
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_update_offer(
        logged_in_user,
        offer_fixture
):
    payload = dict(
        preferred_car={"brand": "foobrand"},
        price=100
    )
    response = client.put(
        reverse('offer-detail', kwargs={"pk": offer_fixture.pk}),
        payload,
        format='json',
        HTTP_AUTHORIZATION=f'Bearer {logged_in_user.get("access")}'
    )

    assert response.status_code == status.HTTP_200_OK
