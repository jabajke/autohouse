import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def payload_fixture():
    payload = dict(
        first_name='Foo',
        last_name='Bar',
        email='foo@bar.com',
        password='foobarpassword',
    )
    return payload


@pytest.fixture
def correct_user_fixture(payload_fixture):
    user = User.objects.create_user(**payload_fixture)
    user.is_active = True
    user.save()
    return user


@pytest.fixture
def wrong_user_fixture(payload_fixture):
    user = User.objects.create_user(**payload_fixture)
    return user
