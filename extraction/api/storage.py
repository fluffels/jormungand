from yapsy import IPlugin

__author__ = 'aj@springlab.co'


class StoragePluginInterface(IPlugin.IPlugin):

    def can_store(self, data_model_name, data_model):
        return False

    def store(self, data_items, data_model_name, data_model):
        return False
