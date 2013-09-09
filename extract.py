from argparse import ArgumentParser
from copy import deepcopy
import sys
from extraction.api import *
from extraction import ExtractionPluginManager
import os
import logging

__author__ = 'aj@springlab.co'


def extract(json_config_file=None, plugin_roots=[], input_files=[], input_directories=[], logging=logging):
    """ Entry-point into the Extraction Process """
    #TODO: Refactor into separate functions or, possibly, a class in the extraction module
    # Init Plugin Manager and Plugins
    logging.info('Initialising Extraction Plugin Manager')
    plugin_manager = ExtractionPluginManager(json_config_file)
    plugin_manager.extendPluginPlaces([os.path.abspath(plugin_root) for plugin_root in plugin_roots])
    plugin_manager.collectPlugins()
    for plugin_info in plugin_manager.getAllPlugins():
        plugin_manager.activatePluginByName(plugin_info.name)
    # Load Data Models
    logging.info('Loading Data Models')
    data_models = {}
    data_templates = {}
    for plugin_info in plugin_manager.getPluginsOfCategory('DataModel'):
        model_name = plugin_info.plugin_object.get_data_model_name()
        data_models[model_name] = plugin_info.plugin_object.get_data_model()
        data_templates[model_name] = plugin_info.plugin_object.get_data_template()
        logging.info('Loaded Data Model %s' % model_name)
    # Obtain a full list of input files
    logging.info('Generating list of files to process')
    for input_directory in input_directories:
        for directory, subdirectories, files in os.walk(input_directory):
            input_files.extend([os.path.join(directory, file) for file in files])
    input_files = [os.path.abspath(input_file) for input_file in input_files]
    logging.info('Finalized list of files to process: %s' % ', '.join(input_files))
    #TODO: A fair bit of repeated code here, refactor
    # Extract data from input files
    logging.info('Extracting data')
    extracted_data = {data_model_name: [] for data_model_name in data_models}
    for plugin_info in plugin_manager.getPluginsOfCategory('Extraction'):
        plugin = plugin_info.plugin_object
        for data_model_name, data_model in data_models.items():
            for input_file in input_files:
                if plugin.can_extract(input_file, data_model_name, data_model):
                    logging.info('Extracting data from %s using Data Model %s and Extraction plugin %s ' % (input_file, data_model_name, plugin))
                    extracted_data[data_model_name].extend(
                        plugin.extract(input_file, data_model_name, data_model, deepcopy(data_templates[data_model_name])))
    # Post-Process
    logging.info('Post-Processing Extracted Data')
    for plugin_info in plugin_manager.getPluginsOfCategory('PostProcessing'):
        plugin = plugin_info.plugin_object
        for data_model_name, data_model in data_models.items():
            if plugin.can_process(data_model_name, data_model):
                logging.info('Post-Processing Data Model %s using Post-Processing plugin %s' % (data_model_name, plugin))
                extracted_data[data_model_name] = plugin.process(extracted_data[data_model_name], data_model_name. data_model)
    # Validation
    logging.info('Validating Extracted Data')
    for plugin_info in plugin_manager.getPluginsOfCategory('Validation'):
        plugin = plugin_info.plugin_object
        for data_model_name, data_model in data_models.items():
            if plugin.can_validate(data_model_name, data_model):
                logging.info('Validating Data Model %s using Validation plugin %s' % (data_model_name, plugin))
                extracted_data[data_model_name] = plugin.validate(extracted_data[data_model_name], data_model_name. data_model)
    # Storage
    logging.info('Storing Extracted Data')
    for plugin_info in plugin_manager.getPluginsOfCategory('Storage'):
        plugin = plugin_info.plugin_object
        for data_model_name, data_model in data_models.items():
            if plugin.can_store(data_model_name, data_model):
                logging.info('Storing items of Data Model %s using Storage plugin %s' % (data_model_name, plugin))
                plugin.store(extracted_data[data_model_name], data_model_name, data_model)


if __name__ == '__main__':
    # Ensure directory of extraction script is on the path
    sys.path.append(os.path.dirname(__file__))
    # Configure CLI parser
    parser = ArgumentParser(description='Extract data from input files into a datastore')
    parser.add_argument('-c', '--config', default=None)
    parser.add_argument('-p', '--pluginroots', dest='plugin_roots', default=[], nargs='*', )
    parser.add_argument('-f', '--inputfiles', dest='input_files', default=[], nargs='*')
    parser.add_argument('-d', '--inputdirectories', dest='input_directories', default=[], nargs='*')
    parser.add_argument('--loglevel', default='INFO')
    args = parser.parse_args()
    # Configure Logging
    logging.basicConfig()
    logging = logging.getLogger('EXTRACTION')
    logging.setLevel(args.loglevel)
    extract(args.config, args.plugin_roots, args.input_files, args.input_directories, logging)

