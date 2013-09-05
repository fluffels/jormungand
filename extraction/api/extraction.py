from yapsy import IPlugin

__author__ = 'aj@springlab.co'


class ExtractedDataItem(dict):
    """
    Overrides the dict class to allow metadata to be added to DataItem dicts by setting attributes on the item. If an
    ExtractedDataItem instance is instantiated using an instance of ExtractedDataItem then the attributes set on the
    input item are copied over to the new item.
    """
    def __init__(self, seq=None, **kwargs):
        super(ExtractedDataItem, self).__init__(seq, **kwargs)
        # If input sequence is an instance of ExtractedDataItem or one of its descendants then copy its custom attributes
        if isinstance(seq, ExtractedDataItem):
            for key, value in vars(seq).items():
                setattr(self, key, value)


class ExtractionPluginInterface(IPlugin.IPlugin):
    """
    Defines an interface for plugins that extract data from a source
    """

    def can_extract(self, source, data_model_name, data_model):
        """
        Determines whether the plugin can extract data for given combination of source and data model. Returns a bool
        """
        return False

    def extract(self, source, data_model_name, data_model, data_template):
        """
        Extract data from a given combination of source and data model.

        Returns a dict mapping UID value -> ExtractedDataItem instance
        """
        return {}

