import os
from jormungand.api import StoragePluginInterface

__author__ = 'aj@springlab.co'


class StatisticsStoragePlugin(StoragePluginInterface):
    """
    A simple Storage Plugin
    """

    def __init__(self, output_path='.'):
        """
        A custom output path prefix may be specific for the data files generated
        """
        self.output_path = output_path

    def can_store(self, data_model_name, data_model):
        """
        The Statistics Storage Plugin can store Statistics for any Data Model
        """
        return True

    def store(self, data_items, data_model_name, data_model):
        """
        Stores Statistics about the Data Items for the associated Data Model
        """
        sources = {}
        uids = {}
        valid = 0
        valid_uids = {}
        validation_errors = {}
        validated_by = {}
        processing_errors = {}
        processed_by = {}
        for uid, data_item in data_items:
            # Generate Statistics
            # UID Statistics
            uids.setdefault(uid, 0)
            uids[uid] += 1
            # Source Statistics
            source = getattr(data_item, 'source', 'unknown')
            source_count = sources.setdefault(source, 0)
            sources[source] = source_count + 1
            # Post-Processing Statistics
            for processor in getattr(data_item, 'processed_by', ['nothing']):
                processed_by.setdefault(processor, 0)
                processed_by[processor] += 1
            for processing_error in getattr(data_item, 'processing_errors', ['none']):
                processing_errors.setdefault(processing_error, 0)
                processing_errors[processing_error] += 1
            # Validation Statistics
            if getattr(data_item, 'valid', True):
                valid += 1
                valid_uids.setdefault(uid, True)
            for validator in getattr(data_item, 'validated_by', ['nothing']):
                validated_by.setdefault(validator, 0)
                validated_by[validator] += 1
            for validation_error in getattr(data_item, 'validation_errors', ['none']):
                validation_errors.setdefault(validation_error, 0)
                validation_errors[validation_error] += 1
        # Store Statistics
        with open(os.path.join(self.output_path, '%s.statistics.txt' % data_model_name), 'wb') as output:
            lines = [
                'Statistics for %s:' % data_model_name,
                '',
                'Totals:',
                'Total data items: %d' % len(data_items),
                'Total valid data items: %d' % valid,
                '',
                'Total unique data_item UIDS: %d' % len(uids),
                'Total valid unique data_item UIDS: %d' % len(valid_uids),
                '',
                'Sources:'
            ] + [
                'Source %s: %s Data Items' % (source, source_count) for source, source_count in sources.items()
            ] + [
                '',
                'Validators:'
            ] + [
                '%s Validated %d Data Items' % (validator, validator_count) for validator, validator_count in validated_by.items()
            ] + [
                '',
                'Validation Errors:'
            ] + [
                '%d %s Validation Errors' % (validation_error, validation_error_count) for validation_error, validation_error_count in validation_errors.items()
            ] + [
                '',
                'Post-Processors:',
            ] + [
                '%s Post-Processed %d Data Items' % (processor, processor_count) for processor, processor_count in processed_by.items()
            ] + [
                '',
                'Post-Processing Errors:'
            ] + [
                '%d %s Post-Processing Errors' % (processor, processor_error_count) for processor, processor_error_count in processing_errors.items()
            ]
            output.writelines('\n'.join(lines))
        return True

