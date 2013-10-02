import logging
from copy import copy
from datetime import datetime
from dateutil import parser
from json import loads, JSONDecoder
from sqlalchemy import create_engine
from extraction.api.datamodel import FieldDefinition
from extraction.api.extraction import ExtractionPluginInterface, ExtractedDataItem
from extraction.plugins.storage.SQLAlchemyFlatStorage import StorageRecord, get_scoped_session

__author__ = 'aj@springlab.co'


def parse_object(o):
    if not hasattr(o, '__class__'):
        return o
    if o['__class__'] == '%s.%s' % (FieldDefinition.__module__, FieldDefinition.__name__):
        #TODO: Lookup type
        return FieldDefinition(default_value=o['default_value'], required=o['required'], unique=o['unique'])
    if o['__class__'] == '%s.%s' % (datetime.__module__, datetime.__name__):
        return parser.parse(o['value'])


class SQLAlchemyFlatStorageSourcePlugin(ExtractionPluginInterface):
    """
    The SQLAlchemyFlatStorageSource provides a means of extracting data that was stored using the
    SQLAlchemyFlatStorage plugin.
    """

    def __init__(self, sqlalchemy_loglevel=None):
        # Init SQLAlchemy
        if sqlalchemy_loglevel:
            logging.getLogger('sqlalchemy.engine').setLevel(sqlalchemy_loglevel)

    def can_extract(self, source, data_model_name, data_model):
        """
        Returns true if the source URL can be transformed into a SQLAlchemy engine instance using create_engine
        """
        try:
            create_engine(source.geturl())
        except:
            return False
        return True

    def extract(self, source, data_model_name, data_model, data_item_template):
        extracted_data = []
        with get_scoped_session(create_engine(source.geturl())) as session:
            for record in session.query(StorageRecord).all():
                extracted_data.append((loads(record.uid, object_hook=parse_object), ExtractedDataItem(vars(record))))
        return extracted_data


