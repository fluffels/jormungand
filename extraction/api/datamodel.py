from yapsy import IPlugin

__author__ = 'aj@springlab.co'


class FieldDefinition(object):

    def __init__(self, type=str, default_value=None, required=False, unique=False):
        self.type = type
        self.default_value = default_value
        self.required = required


class DataModelPluginInterface(IPlugin.IPlugin):

    def get_data_model_name(self):
        return 'modelname'

    def get_data_model(self):
        return {
            'key_field': FieldDefinition(unique=True),
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
        """ Generate a template dictionary object """
        def generate_data_template(data_model):
            template = {}
            for field, field_definition in data_model.items():
                field_value = None
                if isinstance(field_definition, FieldDefinition):
                    try:
                        field_value = field_definition.default_value
                        if not isinstance(field_value, field_definition.type):
                            field_value = field_definition.default_value() if callable(field_definition.default_value) else field_definition.type()
                    except:
                        pass
                elif isinstance(field_definition, (list, dict)):
                    field_definition = field_definition[0] if isinstance(field_definition, list) else field_definition
                    field_value = generate_data_template(field_definition)
                template[field] = field_value
            return template
        return generate_data_template(self.get_data_model())


