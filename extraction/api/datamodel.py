from yapsy import IPlugin

__author__ = 'aj@springlab.co'


class FieldDefinition(object):

    def __init__(self, type=str, default_value=None, required=False):
        self.type = type
        self.default_value = default_value
        self.required = required


class DataModelPluginInterface(IPlugin.IPlugin):

    def get_data_model_name(self):
        return 'modelname'

    def get_data_model(self):
        return {
            'int_field': FieldDefinition(int, required=False),
            'nested_object': {
                'str_field': FieldDefinition(default_value='Yes')

            },
            'nested_array': [FieldDefinition(str)],
            'nested_array_of_objects': [{
                'int_field': FieldDefinition(int, 0),
                'str_field': FieldDefinition()
            }]
        }

    def get_data_template(self):
        #TODO: Generate Template using Model?
        return {
            'int_field': 0,
            'nested_object': {
                'str_field': 'Hello World'
            },
            'nested_array': [
                'Value'
            ],
            'nested_array_of_objects': [{
                'int_field': 0,
                'str_field': ''
            }]
        }


