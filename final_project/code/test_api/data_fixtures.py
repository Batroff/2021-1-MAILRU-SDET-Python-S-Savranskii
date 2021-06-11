import datetime

import pytest
from faker import Faker

from mysql.models import User

fake = Faker()


@pytest.fixture
def test_user():
    username = fake.lexify('??????')
    password = fake.password(length=8)
    email = fake.email()
    access = 1
    active = 0
    start_active_time = datetime.datetime.now()

    return User(
        username=username,
        password=password,
        email=email,
        access=access,
        active=active,
        start_active_time=start_active_time,
    )
