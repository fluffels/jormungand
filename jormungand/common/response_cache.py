from contextlib import contextmanager

import requests

from hashlib import md5

from sqlalchemy import create_engine
from sqlalchemy import Binary
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

RecordBase = declarative_base()


class Response(RecordBase):
    __tablename__ = 'response'
    hash = Column(String(length=32), primary_key=True)
    url = Column(Binary)
    text = Column(Text)


class ResponseCache:
    def __init__(self, rdbms_url='sqlite:///RequestCache.db'):
        self.engine = create_engine(rdbms_url)
        self.session_class = sessionmaker(self.engine)
        RecordBase.metadata.create_all(self.engine)

        @contextmanager
        def session_scope():
            session = self.session_class()
            try:
                yield session
                session.commit()
            except:
                session.rollback()
                raise
            finally:
                session.close()
        self.session_scope = session_scope

    def get_url(self, url):
        url_hash = md5(url).hexdigest()
        with self.session_scope() as session:
            response = session.query(Response.text).filter(
                Response.hash == url_hash).first()
            if not response:
                response = requests.get(url)
                session.add(Response(url=url, hash=url_hash,
                                     text=response.text))
        return response

