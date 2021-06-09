import datetime
import logging

from faker import Faker

from mysql.models import User

fake = Faker()

logger = logging.getLogger('pytest')


class MySQLBuilder:

    def __init__(self, client):
        self.client = client

    def select_user(self, **kwargs):
        """
        :param kwargs:
        :return:
        If filter has unique key return User or None, else List
        """
        self.client.session.commit()

        query = self.client.session.query(User).filter_by(**kwargs)
        if kwargs.get('username') or kwargs.get('email'):
            query = query.one_or_none()

        logger.info(f'Select user query {query}')
        return query

    def create_user(self,
                    username=None,
                    password=None,
                    email=None,
                    access=None,
                    active=None,
                    start_active_time=None,
                    push=True) -> User:

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

        user = User(
            username=username,
            password=password,
            email=email,
            access=access,
            active=active,
            start_active_time=start_active_time,
        )
        logger.info(f'User {user} generated in builder')

        if push:
            self.client.session.add(user)
            self.client.session.commit()
        logger.info(f'User {user.username} inserted in database')

        return user
