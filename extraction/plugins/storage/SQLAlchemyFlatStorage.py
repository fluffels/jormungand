from extraction.api import StoragePluginInterface
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime, BLOB
import json

__author__ = 'aj@spinglab.co'

RecordBase = declarative_base()


class StorageRecord(RecordBase):
    __tablename__ = 'storage'

    datamodel = Column(String, primary_key=True)
    uid = Column(String, primary_key=True)
    version = Column(Integer, primary_key=True)
    created = Column(DateTime)
    data = Column(BLOB)


class SQLAlchemyFlatStoragePlugin(StoragePluginInterface):

    def __init__(self, rdbms_url='sqlite:///SQLAlchemyFlatStoragePlugin.db'):
        #TODO: Init SQLAlchemy
        #TODO: Bind StorageRecord to DB
        #TODO: Create DB Tables if necessary
        pass

    def can_store(self, data_model_name, data_model):
        return True

    def store(self, data_items, data_model_name, data_model):
        return super(SQLAlchemyFlatStoragePlugin, self).store(data_items, data_model_name, data_model)


