from yapsy import IPlugin

__author__ = 'aj@springlab.co'


class ExtractionPluginInterface(IPlugin.IPlugin):

    def can_extract(self, path, data_model_name, data_model):
        return False

    def extract(self, path, data_model_name, data_model, data_template):
        return {}

