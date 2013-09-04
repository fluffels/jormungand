from yapsy import IPlugin
from postprocessing import PostProcessedDataItem

__author__ = 'aj@springlab.co'


class ValidatedDataItem(PostProcessedDataItem):
    def __init__(self, seq=None, **kwargs):
        super(ValidatedDataItem, self).__init__(seq, **kwargs)
        self.valid = False


class ValidationPluginInterface(IPlugin.IPlugin):

    def can_validate(self, data_model_name, data_model):
        return False

    def validate(self, data_item, data_model_name, data_model):
        return ValidatedDataItem(data_item)
