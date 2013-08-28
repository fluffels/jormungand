from yapsy import IPlugin

__author__ = 'aj@springlab.co'


class PostProcessedDataItem(dict):
    def __init__(self, seq=None, **kwargs):
        super(PostProcessedDataItem, self).__init__(seq, **kwargs)


class PostProcessingPluginInterface(IPlugin.IPlugin):

    def can_process(self, data_model_name, data_model):
        return False

    def process(self, data_item, data_model_name, data_model):
        return PostProcessedDataItem(data_item)

