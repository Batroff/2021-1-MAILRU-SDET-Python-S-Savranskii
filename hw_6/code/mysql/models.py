from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class AllRequests(Base):
    __tablename__ = 'all_requests'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f'<AllRequests(' \
               f'id={self.id}, ' \
               f'description={self.description}, ' \
               f'count={self.count}' \
               f')>'

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(50), nullable=False)
    count = Column(Integer, nullable=False)


class RequestsTypes(Base):
    __tablename__ = 'requests_types'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f'<RequestsTypes(' \
               f'id={self.id}, ' \
               f'method={self.method}, ' \
               f'count={self.count}' \
               f')>'

    id = Column(Integer, primary_key=True, autoincrement=True)
    method = Column(String(20), nullable=False)
    count = Column(Integer, nullable=False)


class MostOften(Base):
    __tablename__ = 'most_often'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f'<MostOften(' \
               f'id={self.id}, ' \
               f'url={self.url}, ' \
               f'count={self.count}' \
               f')>'

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(100), nullable=False)
    count = Column(Integer, nullable=False)


class ClientError(Base):
    __tablename__ = 'client_error'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f'<ClientError(' \
               f'id={self.id}, ' \
               f'url={self.url}, ' \
               f'ip={self.ip}, ' \
               f'req_len={self.req_len}, ' \
               f'code={self.code}' \
               f')>'

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(1000), nullable=False)
    ip = Column(String(15), nullable=False)
    req_len = Column(Integer, nullable=False)
    code = Column(Integer, nullable=False)


class ServerError(Base):
    __tablename__ = 'server_error'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f'<ServerError(' \
               f'id={self.id}, ' \
               f'ip={self.ip}, ' \
               f'count={self.count}, ' \
               f')>'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ip = Column(String(15), nullable=False)
    count = Column(Integer, nullable=False)
