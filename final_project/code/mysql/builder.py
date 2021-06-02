import datetime

from faker import Faker

from mysql.models import Users

fake = Faker()


class MySQLBuilder:

    def __init__(self, client):
        self.client = client

    def create_user(self,
                    username=None,
                    password=None,
                    email=None,
                    access=None,
                    active=None,
                    start_active_time=None) -> Users:

        if username is None:
            username = fake.lexify('??????')

        if password is None:
            password = fake.password(length=8)

        if email is None:
            email = fake.email()

        if access is None:
            access = 1

        if active is None:
            active = 0

        if start_active_time is None:
            start_active_time = datetime.datetime.now()

        user = Users(
            username=username,
            password=password,
            email=email,
            access=access,
            active=active,
            start_active_time=start_active_time,
        )
        self.client.session.add(user)
        self.client.session.commit()

        return user
