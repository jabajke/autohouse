import pytest
from django.core.validators import ValidationError
from rest_framework.test import APIClient

from autohouse.models import Autohouse

client = APIClient(HTTP_HOST='localhost')


@pytest.mark.django_db
def test_fail_autohouse_prefer_characteristic():
    exc_msg = '{} failed JSON schema check'
    with pytest.raises(ValidationError) as e:
        characteristic = {
            "color": "foo",
            "body_type": "bar"
        }
        autohouse = Autohouse.objects.create(
            title="FooTitle",
            location="AF",
            prefer_characteristic=characteristic,
            balance=1000.0
        )
        autohouse.full_clean()
    assert exc_msg.format(characteristic) in e.value.messages
