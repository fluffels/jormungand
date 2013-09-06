from contextlib import contextmanager
from datetime import datetime
from extraction.api import StoragePluginInterface
from extraction.api.datamodel import FieldDefinition, generate_field_value
from hashlib import md5
from json import dumps, JSONEncoder
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Integer, DateTime, Binary, create_engine, func
import logging

__author__ = 'aj@spinglab.co'

RecordBase = declarative_base()


class StorageRecord(RecordBase):
    """
    SQLALchemy Record class defining the structure of the table used to store Extracted data
    """
    __tablename__ = 'storage'

    data_model = Column(String)
    data_model_name = Column(String, primary_key=True)
    uid = Column(String, primary_key=True)
    version = Column(Integer, primary_key=True, autoincrement=False)
    created = Column(DateTime, default=datetime.now)
    data_item = Column(Binary)
    data_item_metadata = Column(Binary)
    checksum = Column(String(length=32))


class SQLAlchemyFlatJSONEncoder(JSONEncoder):
    """
    A custom JSONEncoder that is capable of handling the FieldDefinition classes included within the Data Model
    """

    def __init__(self, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, sort_keys=False,
                 indent=4, separators=(',', ':'), encoding='utf-8', default=None):
        """
        Init is overridden to specify indent
        """
        super(SQLAlchemyFlatJSONEncoder, self).__init__(skipkeys, ensure_ascii, check_circular, allow_nan, sort_keys,
                                                        indent, separators, encoding, default)

    def default(self, o):
        """
        Custom default implementation that handles FieldDefinition and datetime instances
        """
        if isinstance(o, FieldDefinition):
            return {
                '__class__': '%s.%s' % (FieldDefinition.__module__, FieldDefinition.__name__),
                'type': '%s.%s' % (o.type.__module__, o.type.__name__),
                'default_value': generate_field_value(o),
                'required': o.required,
                'unique': o.unique

            }
        if isinstance(o, datetime):
            return o.isoformat()
        return super(SQLAlchemyFlatJSONEncoder, self).default(o)


class SQLAlchemyFlatJSONStoragePlugin(StoragePluginInterface):
    """
    The SQLAlchemyFlatJSONStoragePlugin provides a means of storing generic data in a database using SQLAlchemy.

    Data is converted to JSON format and stored in BLOBs, along with additional useful information that should
    allow for the stored data to be re-used and accessed easily enough.
    """

    def __init__(self, rdbms_url='sqlite:///SQLAlchemyFlatStoragePlugin.db', sqlalchemy_loglevel=None):
        # Init SQLAlchemy
        self.engine = create_engine(rdbms_url)
        if sqlalchemy_loglevel:
            logging.getLogger('sqlalchemy.engine').setLevel(sqlalchemy_loglevel)
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
            data_model = dumps(data_model, cls=SQLAlchemyFlatJSONEncoder)
            uid_version_checksums = {
                (uid, version): checksum for uid, version, checksum in session
                    .query(StorageRecord.uid, StorageRecord.version, StorageRecord.checksum)
                    .filter(StorageRecord.data_model_name == data_model_name)
            }
            current_versions = {
                uid: (version, uid_version_checksums.get((uid, version))) for uid, version in session
                    .query(StorageRecord.uid, func.max(StorageRecord.version))
                    .filter(StorageRecord.data_model_name == data_model_name)
                    .group_by(StorageRecord.uid)
            }
            for uid, data_item in data_items:
                uid, data_item, data_item_metadata = \
                    [dumps(item, cls=SQLAlchemyFlatJSONEncoder) for item in (uid, data_item, vars(data_item))]
                checksum = md5('#'.join([data_model, data_item, data_item_metadata])).hexdigest()
                current_version, current_version_checksum = current_versions.get(uid, (0, None))
                if checksum == current_version_checksum:
                    continue
                current_versions[uid] = (current_version + 1, checksum)
                session.add(StorageRecord(data_model=data_model, data_model_name=data_model_name, uid=uid,
                                          version=current_version + 1, data_item=data_item, checksum=checksum,
                                          data_item_metadata=data_item_metadata))
        return super(SQLAlchemyFlatJSONStoragePlugin, self).store(data_items, data_model_name, data_model)


