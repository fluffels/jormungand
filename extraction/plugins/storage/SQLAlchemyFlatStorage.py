from contextlib import contextmanager
from datetime import datetime
from extraction.api import StoragePluginInterface
from json import dumps
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Integer, DateTime, Binary, create_engine, func

__author__ = 'aj@spinglab.co'

RecordBase = declarative_base()


class StorageRecord(RecordBase):
    __tablename__ = 'storage'

    data_model = Column(String)
    data_model_name = Column(String, primary_key=True)
    uid = Column(String, primary_key=True)
    version = Column(Integer, primary_key=True, autoincrement=False)
    created = Column(DateTime, default=datetime.now)
    data_item = Column(Binary)
    data_item_metadata = Column(Binary)


class SQLAlchemyFlatJSONStoragePlugin(StoragePluginInterface):
    """
    The SQLAlchemyFlatJSONStoragePlugin provides a means of storing generic data in a database using SQLAlchemy.

    Data is converted to JSON format and stored in BLOBs, along with additional useful information that should
    allow for the stored data to be re-used and accessed easily enough.
    """

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
        with self.session_scope() as session:
            data_model = dumps(data_model)
            current_versions = {
                uid: version for uid, version in session
                    .query(StorageRecord.uid, func.max(StorageRecord.version))
                    .filter(StorageRecord.data_model_name == data_model_name)
                    .group_by(StorageRecord.uid)
            }
            for uid, data_item in data_items.items():
                uid = dumps(uid)
                session.add(StorageRecord(data_model=data_model, data_model_name=data_model_name, uid=uid,
                                          version=current_versions.get(uid, 0) + 1, data_item=dumps(data_item),
                                          data_item_metadata=dumps(vars(data_item))))
        return super(SQLAlchemyFlatJSONStoragePlugin, self).store(data_items, data_model_name, data_model)


