#
# Copyright (C) 2019 IHS Markit.
# All Rights Reserved
#

from ..logging import UnparsableNamespaceFilter


class LoggingRecord:
    def __init__(self, locals_):
        self.locals = locals_


class TestUnparsableNamespaceFilter:

    def test_filters_out_keys_that_are_types_from_record_locals(self):
        tested_filter = UnparsableNamespaceFilter()
        dict_to_filter = {
            type: 'value1',
            'key2': {
                LoggingRecord: 'value2',
                'key2b': 'value3'
            },
            3: 'value4',
            True: 'value5',
            5.0: 'value6',
            False: {
                True: True,
                False: {
                    object: 'abc',
                    'key6b1': 'value9'
                }
            }
        }
        record = LoggingRecord(locals_=dict_to_filter)
        tested_filter.filter(record)

        assert record.locals == {
            'key2': {
                'key2b': 'value3'
            },
            3: 'value4',
            True: 'value5',
            5.0: 'value6',
            False: {
                True: True,
                False: {
                    'key6b1': 'value9'
                }
            }
        }

    def test_does_not_fail_if_no_locals_specified(self):
        tested_filter = UnparsableNamespaceFilter()
        tested_filter.filter(object())

        assert True
