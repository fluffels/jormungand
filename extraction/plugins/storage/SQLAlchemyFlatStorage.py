from contextlib import contextmanager
from datetime import datetime
from extraction.api import StoragePluginInterface
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Integer, DateTime, BLOB, create_engine
import json

__author__ = 'aj@spinglab.co'

RecordBase = declarative_base()


class StorageRecord(RecordBase):
    __tablename__ = 'storage'

    datamodel = Column(String)
    datamodel_name = Column(String, primary_key=True)
    uid = Column(String, primary_key=True)
    version = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.now)
    data_item = Column(BLOB)


class SQLAlchemyFlatJSONStoragePlugin(StoragePluginInterface):

    def __init__(self, rdbms_url='sqlite:///SQLAlchemyFlatStoragePlugin.db'):
        # Init SQLAlchemy
        self.engine = create_engine(rdbms_url)
        self.session_class = sessionmaker(self.engine)
        RecordBase.metadata.create_all(self.engine)
        # Define ContextManager
        @contextmanager
        def session_scope():
            """Provide a transactional scope around a series of operations."""
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

    def can_store(self, data_model_name, data_model):
        return True

    def store(self, data_items, data_model_name, data_model):
        return super(SQLAlchemyFlatJSONStoragePlugin, self).store(data_items, data_model_name, data_model)


