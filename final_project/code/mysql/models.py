from sqlalchemy import Column, Integer, String, SmallInteger, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Users(Base):
    __tablename__ = 'test_users'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f'<(' \
               f'id: {self.id}, ' \
               f'username: {self.username}, ' \
               f'password: {self.password}, ' \
               f'email: {self.email}, ' \
               f'access: {self.access}, ' \
               f'active: {self.active}, ' \
               f'start_active_time: {self.start_active_time}' \
               f')>'

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    username = Column(String(16), default='', unique=True)  # null login? bug
    password = Column(String(255), nullable=False, unique=True)
    email = Column(String(64), nullable=False)
    access = Column(SmallInteger, default=None)
    active = Column(SmallInteger, default=None)
    start_active_time = Column(DateTime, default=None)
