#
# Copyright (C) 2019 IHS Markit.
# All Rights Reserved
#
import os
import boto3
import mock
import pytest
import numpy as np
import itertools
import datetime
from functools import partial
from unittest.mock import MagicMock
from collections import namedtuple
from typing import List
# from cachetools import TTLCache
from dateutil.tz import tzutc
from freezegun import freeze_time
from unittest.mock import Mock
from moto import mock_sts

from ..services.consumption_service.consumption_dataset_handler import ConsumptionDatasetHandler
from ..services.consumption_service.file_service import DISPATCHER

from ..handlers.s3_dataset_handler import S3DatasetHandler
from ..handlers.s3_partition_handler import meets_partition_params
from ..services.consumption_service.file_service import FileService
from ..services.exceptions import UnableToAccessDataset, UnableToParsePartition

path_with_as_of_date = 'prefix/a=2/b=4/c=6/as_of_date=2020-01-23/file.ext'
path_with_as_of_year_month = 'prefix/a=2/b=4/c=6/' \
                             'as_of_year_month=2020-01/file.ext'


@pytest.fixture
def dlc_service_with_mock(aws_s3, dataset_response, dlc_service):

    dlc_service.get_dataset.return_value = dataset_response

    dlc_service.get_datafile.return_value = {
        'properties': {
            'datasetId': 'abc',
            'files': [
                {
                    'path': (
                        's3://bucket/prefix/'
                        'datafile/a=1/path/parquet.parquet'
                    ),
                    # noqa
                    'size': 100
                },
            ]
        }
    }

    yield dlc_service


@pytest.fixture
def object_summaries_on_s3(aws_s3, request):
    # SEE difference to object_summaries `s3_resource.Object('bucket', path).put(`

    file_ = getattr(request, 'param', 'nulls_and_unicode.parquet')

    # path depends on whether running from top-level or not (PyCharm debug vs. pytest command line)
    path = os.path.join(f"{os.getcwd()}/lib/tests/data/parquet_stress_test/{file_}")
    if not os.path.exists(path):
        path = os.path.join(f"{os.getcwd()}/data/parquet_stress_test/{file_}")

    with open(path, 'rb') as f:
        file_data = f.read()

    with freeze_time('2020-01-01T00:00:00Z'):
        s3_resource = boto3.resource('s3')
        bucket = s3_resource.create_bucket(Bucket='bucket', CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'},)

        s3_resource.Object('bucket', f'prefix/as_of_date=2020-01-01/{file_}').put(
            Body=file_data
        )

    yield [f for f in bucket.objects.all()]


@pytest.fixture
def platform_app_client_with_handler(platform_app_blueprint):
    platform_app_blueprint.injector.binder.bind(DISPATCHER, to=ConsumptionDatasetHandler)
    yield platform_app_blueprint.test_client()


@pytest.fixture
def dataset_response():
    return {
        'id': 'abc',
        'attributes': {
            'content_type': "Structured",
            'location': {
                's3': {
                    'type': 's3',
                    'bucket': 'bucket',
                    'prefix': 'prefix',
                    'aws_role_arn': 'arn:aws:iam::000000000001:user/root',
                    'owner': {"tim"},
                },
            },
            'data_format': 'parquet',
            'name': 'test_dataset',
            'organisation_short_code': 'abc',
            'short_code': 'abc',
            'has_access': True,
            'load_type': 'Full Load',
        }
    }


@pytest.fixture
def dataset_response_location_other():
    return {
        'id': 'abc',
        'attributes': {
            'content_type': "Structured",
            'location': {
                'other': {
                    'type': 's3',
                    'bucket': 'bucket',
                    'prefix': 'prefix',
                    'aws_role_arn': 'arn:aws:iam::000000000001:user/root',
                    'owner': {"tim"},
                },
            },
            'data_format': 'parquet',
            'name': 'test_dataset',
            'organisation_short_code': 'abc',
            'short_code': 'abc',
            'has_access': True,
            'load_type': 'Full Load',
        }
    }


@pytest.fixture
def dataset_response_location_s3_and_other():
    return {
        'id': 'abc',
        'attributes': {
            'content_type': "Structured",
            'location': {
                's3': {
                    'type': 's3',
                    'bucket': 'bucket',
                    'prefix': 'prefix',
                    'aws_role_arn': 'arn:aws:iam::000000000001:user/root',
                    'owner': {"tim"},
                },
                'other': {
                    'type': 's3',
                    'bucket': 'bucket',
                    'prefix': 'prefix',
                    'aws_role_arn': 'arn:aws:iam::000000000001:user/root',
                    'owner': {"tim"},
                },
            },
            'data_format': 'parquet',
            'name': 'test_dataset',
            'organisation_short_code': 'abc',
            'short_code': 'abc',
            'has_access': True,
            'load_type': 'Full Load',
        }
    }


@pytest.fixture
def dataset_response_full_load():
    return {
        'id': 'abc',
        'attributes': {
            'content_type': "Structured",
            'location': {
                's3': {
                    'type': 's3',
                    'bucket': 'bucket',
                    'prefix': 'prefix',
                    'aws_role_arn': 'arn:aws:iam::000000000001:user/root',
                    'owner': {},
                },
            },
            'organisation_short_code': 'abc',
            'short_code': 'abc',
            'has_access': True,
            'data_format': 'parquet',
            'name': 'test_dataset_full',
            'load_type': 'Full Load',
        }
    }


@pytest.fixture
def dataset_response_incremental_load():
    return {
        'id': 'abc',
        'attributes': {
            'content_type': "Structured",
            'location': {
                's3': {
                    'type': 's3',
                    'bucket': 'bucket',
                    'prefix': 'prefix',
                    'aws_role_arn': 'arn:aws:iam::000000000001:user/root',
                    'owner': {},
                },
            },
            'organisation_short_code': 'abc',
            'short_code': 'abc',
            'has_access': True,
            'load_type': 'Incremental Load',
            'data_format': 'parquet',
            'name': 'test_dataset_incremental',
        }
    }


@pytest.fixture
def unstructured_dataset_response():
    return {
        'id': 'abc',
        'attributes': {
            'content_type': "Unstructured",
            'location': {
                's3': {
                    'type': 's3',
                    'bucket': 'bucket',
                    'prefix': 'prefix',
                    'aws_role_arn': 'arn:aws:iam::000000000001:user/root',
                    'owner': {},
                }
            },
            'organisation_short_code': 'abc',
            'short_code': 'abc',
            'has_access': True,
            'load_type': 'Full Load',
        }
    }


@pytest.fixture
def partition_object(aws_s3, request):
    file_ = getattr(request, 'param', 'nulls_and_unicode.parquet')

    # path depends on whether running from top-level or not (PyCharm debug vs. pytest command line)
    path = os.path.join(f"{os.getcwd()}/lib/tests/data/parquet_stress_test/{file_}")
    if not os.path.exists(path):
        path = os.path.join(f"{os.getcwd()}/data/parquet_stress_test/{file_}")
    with open(path, 'rb') as f:
        file_data = f.read()

    with freeze_time('2020-01-01T00:00:00Z'):
        s3_resource = boto3.resource('s3')
        bucket = s3_resource.create_bucket(Bucket='bucket',
                                           CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'},)

        s3_resource.Object(
            'bucket',
            f'prefix/a=2/b=4/c=6/as_of_date=2020-01-23/{file_}'
        ).put(
            Body=file_data
        )

    yield [f for f in bucket.objects.all()]


@mock_sts
class TestFileService:

    @pytest.fixture
    def file_service(self, dlc_service, platform_app_client_with_handler):
        yield FileService(
            dlc_service=dlc_service,
        )

    def test_get_handler_location_s3(self, dataset_response, file_service):
        s3_handler_mock = MagicMock()
        file_service.stream_handlers['s3'] = s3_handler_mock
        handler = file_service.get_handler(dataset_response)
        assert handler == s3_handler_mock

    def test_get_handler_location_s3_and_other(self, dataset_response_location_s3_and_other, file_service):
        s3_handler_mock = MagicMock()
        file_service.stream_handlers['s3'] = s3_handler_mock
        handler = file_service.get_handler(dataset_response_location_s3_and_other)
        assert handler == s3_handler_mock

    def test_get_handler_location_other(self, dataset_response_location_other, file_service):
        s3_handler_mock = MagicMock()
        file_service.stream_handlers['s3'] = s3_handler_mock
        with pytest.raises(UnableToAccessDataset):
            file_service.get_handler(dataset_response_location_other)

    def test_get_files(
            self, object_summaries_on_s3, dataset_response, file_service,
    ):
        files = list(
            file_service.get_files_from_dataset(
                dataset=dataset_response,
            )
        )
        assert files[0].size == object_summaries_on_s3[0].size
        assert files[0].path == object_summaries_on_s3[0].key

    def test_get_multiple_files(
            self, object_summaries_on_s3, dataset_response, file_service,
    ):
        s3_resource = boto3.resource('s3')
        s3_object = object_summaries_on_s3[0]

        for i in range(10):
            s3_resource.Bucket(
                s3_object.bucket_name
            ).copy(
                CopySource={
                    'Bucket': s3_object.bucket_name,
                    'Key': s3_object.key
                },
                Key=f'prefix/as_of_date=2021-01-01/nulls_and_unicode.{i}.parquet'
            )

        files = list(file_service.get_files_from_dataset(
            dataset=dataset_response,
        ))
        assert len(files) == 10

    def test_fetch_single_file_in_list(
            self, object_summaries_on_s3, dataset_response, file_service,
    ):
        files = list(file_service.get_files_from_dataset(
            dataset=dataset_response,
            paths=['prefix/as_of_date=2020-01-01/nulls_and_unicode.parquet'],
        ))

        assert files[0].path == object_summaries_on_s3[0].key

    def test_nothing_is_returned_for_invalid_path(
            self, object_summaries_on_s3, dataset_response, file_service,
    ):
        files = list(file_service.get_files_from_dataset(
            dataset=dataset_response,
            paths=['prefix/not_a_real_path'],
        ))

        assert len(files) == 0

    def test_can_filter_by_path_and_partition(
            self, object_summaries_on_s3, dataset_response, file_service,
    ):
        s3_resource = boto3.resource('s3')
        s3_object = object_summaries_on_s3[0]
        s3_resource.Bucket(
            s3_object.bucket_name
        ).copy(
            CopySource={
                'Bucket': s3_object.bucket_name,
                'Key': s3_object.key,#'prefix/as_of_date=2020-01-01/nulls_and_unicode.parquet'
            },
            Key=(
                'prefix/a=1/test.parquet'
            )
        )

        files = list(file_service.get_files_from_dataset(
            dataset=dataset_response,
            partitions=[{'partition': 'a', 'operator': "=", 'value': '1'}],
            paths=['prefix/as_of_date=2020-01-01/nulls_and_unicode.parquet'],
        ))

        # includes nulls_and_unicode
        assert len(files) == 1

        files = list(file_service.get_files_from_dataset(
            dataset=dataset_response,
            partitions=[{'partition': 'a', 'operator': "!=", 'value': '1'}],
            paths=['prefix/not_a_path'],
        ))

        assert len(files) == 0

    def test_get_partitions_from_dataset(
            self, object_summaries_on_s3, dataset_response, file_service,
    ):
        _regions = ['US', 'EU', 'CN', 'JP', 'UK']
        _dates = np.arange(np.datetime64('2020-01-01'),
                           np.datetime64('2020-01-11'))
        dates = [
            x.astype(datetime.datetime).strftime("%Y%m%d") for x in _dates
        ]

        dates = ['2020-01-01' for _ in range(len(_regions))]
        items = list(itertools.product(dates, _regions))

        s3_resource = boto3.resource('s3')
        s3_object = object_summaries_on_s3[0]
        for item in items:
            s3_resource.Bucket(
                s3_object.bucket_name
            ).copy(
                CopySource={
                    'Bucket': s3_object.bucket_name,
                    'Key': s3_object.key,
                },
                Key=(
                    f'prefix/'
                    f'as_of_date={item[0]}/'
                    f'country={item[1]}/test.parquet'
                )
            )

        partitions = file_service.get_partitions_from_dataset(
            dataset=dataset_response,
        )
        assert (
                partitions.get('as_of_date') is not None
                and partitions.get('country') is not None
        )
        assert (
                all(elem in partitions.get('as_of_date') for elem in dates)
                and all(elem in partitions.get('country') for elem in _regions)
        )

    def test_filter_by_datafile(
            self, dlc_service_with_mock, file_service, aws_s3
    ):
        s3_resource = boto3.resource('s3')
        bucket = s3_resource.create_bucket(Bucket='bucket',
                                           CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'}, )  # noqa
        s3_resource.Object('bucket', 'prefix/datafile/a=1/path/parquet.parquet').put(
            Body=b'NOOP'
        )

        files = list(file_service.get_files_from_datafile(
            datafile_id='abc',
        ))
        assert len(files) == 1

    def test_restricted_dataset(self, file_service):
        restricted_dataset = {
            'id': 'abc',
            'attributes': {
            }
        }

        with pytest.raises(UnableToAccessDataset):
            list(
                file_service.get_files_from_dataset(dataset=restricted_dataset)
            )

    def test_no_arn_on_dataset(self, object_summaries_on_s3, file_service):
        incomplete_dataset = {
            'id': 'abc',
            'attributes': {
                'location': {
                    's3': {
                        'aws_role_arn': None
                    }
                }
            }
        }

        with pytest.raises(Exception):
            list(
                file_service.get_files_from_dataset(
                    dataset=incomplete_dataset
                )
            )

    def test_partition_matches(
            self, aws_s3, partition_object, dataset_response, file_service
    ):
        files = list(
            file_service.get_files_from_dataset(
                dataset=dataset_response,
                partitions=[{
                    'partition': 'a',
                    'operator': '=',
                    'value': '2'
                }],
            )
        )

        assert len(files) == 1

    def test_partition_does_not_match(
            self, partition_object, dataset_response, file_service
    ):
        files = list(file_service.get_files_from_dataset(
            dataset=dataset_response,
            partitions=[{
                'partition': 'a',
                'operator': '=',
                'value': 'not a match'
            }],
        ))

        assert len(files) == 0

    @pytest.mark.parametrize(
        'path,partitionquery', [
            [
                path_with_as_of_date,
                [{'partition': 'a', 'operator': '<', 'value': '3'}],
            ],

            [
                path_with_as_of_date,
                [{'partition': 'b', 'operator': '=', 'value': '4'}],
            ],

            [
                path_with_as_of_date,
                [{'partition': 'c', 'operator': ">", 'value': '5'}],
            ],

            [
                path_with_as_of_date,
                [{'partition': 'd', 'operator': "!=", 'value': '5'}],
            ],

            [
                path_with_as_of_date,
                [{'partition': 'as_of_date', 'operator': '=',
                  'value': '2020-01-23'}],
            ],
            [
                path_with_as_of_year_month,
                [{'partition': 'as_of_year_month', 'operator': '=',
                  'value': '2020-01'}],
            ],

            # Combination of all filters.
            [
                path_with_as_of_date,
                [{'partition': 'a', 'operator': '<', 'value': '3'},
                 {'partition': 'b', 'operator': '=', 'value': '4'},
                 {'partition': 'c', 'operator': ">", 'value': '5'},
                 {'partition': 'as_of_date', 'operator': '=',
                  'value': '2020-01-23'}],
            ],
            [
                path_with_as_of_year_month,
                [{'partition': 'a', 'operator': '<', 'value': '3'},
                 {'partition': 'b', 'operator': '=', 'value': '4'},
                 {'partition': 'c', 'operator': ">", 'value': '5'},
                 {'partition': 'as_of_year_month', 'operator': '=',
                  'value': '2020-01'}],
            ],
        ],
    )
    def test_meets_partition_params(
            self, path: str, partitionquery: List
    ):
        assert meets_partition_params(path, partitionquery)

    @pytest.mark.parametrize(
        'path,partitionquery',
        [
            [
                path_with_as_of_date,
                [{'partition': 'a', 'operator': '>', 'value': '3'}],
            ],

            [
                path_with_as_of_date,
                [{'partition': 'c', 'operator': "<", 'value': '5'}],
            ],

            [
                path_with_as_of_date,
                [{'partition': 'as_of_date', 'operator': '<',
                  'value': '2020-01-23'}],
            ],
            [
                path_with_as_of_year_month,
                [{'partition': 'as_of_year_month', 'operator': '<',
                  'value': '2020-01'}],
            ],

            [
                path_with_as_of_date,
                [{'partition': 'as_of_date', 'operator': '>',
                  'value': '2020-01-23'}],
            ],
            [
                path_with_as_of_year_month,
                [{'partition': 'as_of_year_month', 'operator': '>',
                  'value': '2020-01'}],
            ],
        ],
    )
    def test_fails_partition_params(
            self, path: str, partitionquery: List
    ):
        assert not meets_partition_params(path, partitionquery)

    @pytest.mark.parametrize(
        'path,partitionquery',
        [
            [
                path_with_as_of_date,
                [
                    {'partition': 'as_of_date', 'operator': '=',
                     'value': '2020-01-23'}
                ]
            ],
            # Left starts with space
            [
                path_with_as_of_date,
                [{'partition': ' as_of_date', 'operator': '=',
                  'value': '2020-01-23'}
                 ]
            ],
            # Left ends with space
            [
                path_with_as_of_date,
                [{'partition': 'as_of_date ', 'operator': '=',
                  'value': '2020-01-23'}
                 ]
            ],
            # Left starts and ends with space
            [
                path_with_as_of_date,
                [{'partition': ' as_of_date ', 'operator': '=',
                  'value': '2020-01-23'}
                 ]
            ],
            # Right starts with space
            [
                path_with_as_of_date,
                [{'partition': 'as_of_date', 'operator': '=',
                  'value': ' 2020-01-23'}
                 ]
            ],
            # Right ends with space
            [
                path_with_as_of_date,
                [{'partition': 'as_of_date', 'operator': '=',
                  'value': '2020-01-23 '}
                 ]
            ],
            # Right starts and ends with space
            [
                path_with_as_of_date,
                [{'partition': 'as_of_date', 'operator': '=',
                  'value': ' 2020-01-23 '}
                 ]
            ],

            # Left starts with space
            [
                path_with_as_of_year_month,
                [{'partition': ' as_of_year_month', 'operator': '=',
                  'value': '2020-01'}
                 ]
            ],
            # Left ends with space
            [
                path_with_as_of_year_month,
                [{'partition': 'as_of_year_month ', 'operator': '=',
                  'value': '2020-01'}
                 ]
            ],
            # Left starts and ends with space
            [
                path_with_as_of_year_month,
                [{'partition': ' as_of_year_month ', 'operator': '=',
                  'value': '2020-01'}
                 ]
            ],
            # Right starts with space
            [
                path_with_as_of_year_month,
                [{'partition': 'as_of_year_month', 'operator': '=',
                  'value': ' 2020-01'}
                 ]
            ],
            # Right ends with space
            [
                path_with_as_of_year_month,
                [{'partition': 'as_of_year_month', 'operator': '=',
                  'value': '2020-01 '}
                 ]
            ],
            # Right starts and ends with space
            [
                path_with_as_of_year_month,
                [{'partition': 'as_of_year_month', 'operator': '=',
                  'value': ' 2020-01 '}
                 ]
            ],
        ]
    )
    def test_meets_date_supported_partition_params(
            self, path: str, partitionquery: List
    ):
        assert meets_partition_params(path, partitionquery)

    def test_filtering_combinations(
            self, partition_object, dataset_response, file_service
    ):
        files = list(file_service.get_files_from_dataset(
            dataset=dataset_response,
            partitions=[{
                'partition': 'a',
                'operator': '=',
                'value': 'not a match'
            }],
        ))

        assert len(files) == 0

    def test_skip_dot_files(
            self, dataset_response, file_service, aws_s3
    ):
        s3_resource = boto3.resource('s3')
        bucket = s3_resource.create_bucket(Bucket='bucket', CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'},)  # noqa
        s3_resource.Object('bucket', 'prefix/.hidden_file').put(
            Body=b'NOOP'
        )

        files = list(file_service.get_files_from_dataset(
            dataset=dataset_response,
            skip_hidden_files=True,
        ))

        assert len(files) == 0

    def test_do_not_skip_dot_files_by_default(
            self, dataset_response, file_service, aws_s3
    ):
        s3_resource = boto3.resource('s3')
        bucket = s3_resource.create_bucket(Bucket='bucket', CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'},)  # noqa
        s3_resource.Object('bucket', 'prefix/.hidden_file').put(
            Body=b'NOOP'
        )
        s3_resource.Object('bucket', 'prefix/as_of_date=2021-04-01/nulls_and_unicode.parquet').put(
            Body=b'NOOP'
        )

        files = list(file_service.get_files_from_dataset(
            dataset=dataset_response,
            # NOTE: skip_hidden_files=False by default
        ))
        assert len(files) == 1

    def test_skip_files_in_dot_dirs(
            self, dataset_response, file_service, aws_s3
    ):
        s3_resource = boto3.resource('s3')
        bucket = s3_resource.create_bucket(Bucket='bucket', CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'},)  # noqa
        s3_resource.Object('bucket', 'prefix/.hidden/normal').put(
            Body=b'NOOP'
        )

        files = list(file_service.get_files_from_dataset(
            dataset=dataset_response,
            skip_hidden_files=True,
        ))

        assert len(files) == 0

    def test_skip_files_in_spark_meta_dirs(
            self, dlc_service, platform_app_blueprint,
            dataset_response, file_service, aws_s3
    ):
        s3_resource = boto3.resource('s3')
        bucket = s3_resource.create_bucket(Bucket='bucket', CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'},)  # noqa
        s3_resource.Object('bucket', 'prefix/_spark_metadata/normal').put(
            Body=b'NOOP'
        )
        s3_resource.Object('bucket', 'prefix/_metadata/normal').put(
            Body=b'NOOP'
        )
        s3_resource.Object('bucket', 'prefix/metadata/normal').put(
            Body=b'NOOP'
        )

        files = list(file_service.get_files_from_dataset(
            dataset=dataset_response,
            skip_hidden_files=True,
            skip_special_hadoop_files=True,
        ))

        assert len(files) == 0, 'Must be empty, but contained this Spark ' \
                                f'metadata cruft: {files}'

    def test_non_skip_metadata_when_unstructured(
            self, dlc_service, platform_app_blueprint, dataset_response,
            unstructured_dataset_response, file_service, aws_s3
    ):
        s3_resource = boto3.resource('s3')
        bucket = s3_resource.create_bucket(Bucket='bucket', CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'},)  # noqa
        s3_resource.Object('bucket', 'prefix/metadata/normal').put(
            Body=b'NOOP'
        )

        files = list(file_service.get_files_from_dataset(
            dataset=unstructured_dataset_response,
            skip_hidden_files=True,
            skip_special_hadoop_files=True,
        ))

        assert len(files) == 1, 'Must be empty, but contained this Spark ' \
                                f'metadata cruft: {files}'

        files = list(file_service.get_files_from_dataset(
            dataset=dataset_response,
            skip_hidden_files=True,
            skip_special_hadoop_files=True,
        ))

        assert len(files) == 0, 'Must be empty, but contained this Spark ' \
                                f'metadata cruft: {files}'

    def test_skip_hidden_folders_and_files_full_load(
            self, monkeypatch, dataset_response_full_load, file_service, object_summaries_on_s3
    ):
        s3_resource = boto3.resource('s3')
        s3_object = object_summaries_on_s3[0]
        paths = ['prefix/.latest/',
                 'prefix/.hidden',
                 'prefix/as_of_date=2021-01-01/',
                 'prefix/as_of_date=2021-02-01/',
                 'prefix/as_of_date=2021-03-01/',
                 'prefix/as_of_date=2021-03-01/a.parquet',
                ]

        for path in paths:
            s3_resource.Bucket(
                s3_object.bucket_name
            ).copy(
                CopySource={
                    'Bucket': s3_object.bucket_name,
                    'Key': s3_object.key
                },
                Key=path
            )

        old_filter = file_service.stream_handlers['s3'].get_s3_list_filter
        file_service.stream_handlers['s3'].get_s3_list_filter = MagicMock()

        list(file_service.get_files_from_dataset(
            dataset=dataset_response_full_load,
        ))

        file_service.stream_handlers['s3'].get_s3_list_filter.assert_called_with(
            s3_resource,
            absolute_path=False,
            bucket_name=s3_object.bucket_name,
            prefix='prefix/',
            prefix_filter_fn=mock.ANY
        )

        file_service.stream_handlers['s3'].get_s3_list_filter = old_filter
        filtered = file_service.stream_handlers['s3'].get_s3_list_filter(
            s3_resource,
            absolute_path=False,
            bucket_name=s3_object.bucket_name,
            prefix='prefix/',
            prefix_filter_fn=partial(
                    S3DatasetHandler.filter_hidden_prefixes_by_dataset_content_and_load_type,
                    dataset_response_full_load['attributes']["content_type"],
                    dataset_response_full_load['attributes']["load_type"],
                    "prefix/",
                    True,
                    None,
                )
        )

        filtered = [x['Key'] for x in filtered]
        assert filtered == ['prefix/as_of_date=2021-03-01/a.parquet']

    def test_skip_hidden_folders_and_files_incremental_load(
            self, monkeypatch, dataset_response_incremental_load, file_service, object_summaries_on_s3
    ):
        s3_resource = boto3.resource('s3')
        s3_object = object_summaries_on_s3[0]
        paths = ['prefix/.latest/',
                 'prefix/.latest/country=UK/',
                 'prefix/.latest/country=US/',
                 'prefix/.hidden',
                 'prefix/as_of_date=2021-01-01/',
                 'prefix/as_of_date=2021-01-01/a.parquet',
                 'prefix/as_of_date=2021-02-01/b.parquet',
                 'prefix/as_of_date=2021-03-01/c.parquet']
        for path in paths:
            s3_resource.Bucket(
                s3_object.bucket_name
            ).copy(
                CopySource={
                    'Bucket': s3_object.bucket_name,
                    'Key': s3_object.key
                },
                Key=path
            )

        filtered = file_service.stream_handlers['s3'].get_s3_list_filter(
            s3_resource,
            absolute_path=False,
            bucket_name=s3_object.bucket_name,
            prefix='prefix/',
            prefix_filter_fn=partial(
                S3DatasetHandler.filter_hidden_prefixes_by_dataset_content_and_load_type,
                dataset_response_incremental_load['attributes']["content_type"],
                dataset_response_incremental_load['attributes']["load_type"],
                "prefix/",
                True,
                None,
            )
        )

        filtered = [x['Key'] for x in filtered]
        assert(len(filtered) == 4) #todo specify a,b,c and nulls [from object_summaries_on_s3 magic weirdness]

    def test_skip_latest_folders_and_files_full_load(
            self, monkeypatch, dataset_response_full_load, file_service, object_summaries_on_s3
    ):
        s3_resource = boto3.resource('s3')
        s3_object = object_summaries_on_s3[0]

        paths = [
            'prefix/as_of_date=latest/',
            'prefix/as_of_year_month=latest/',
            'prefix/as_of_year_month=latest', # this is a weird file - proves doesnt enter is_hidden_prefix (as not retrieved from s3)
            # NOTE: if as_of_date is a partition it will be top level
            'prefix/as_of_date=2021-03-01/',
            'prefix/as_of_date=2021-03-01/a.parquet',
            'prefix/as_of_date=2021-02-01/',
            'prefix/as_of_date=2021-01-01/',
        ]
        for path in paths:
            s3_resource.Bucket(
                s3_object.bucket_name
            ).copy(
                CopySource={
                    'Bucket': s3_object.bucket_name,
                    'Key': s3_object.key
                },
                Key=path
        )

        filtered = file_service.stream_handlers['s3'].get_s3_list_filter(
            s3_resource,
            absolute_path=False,
            bucket_name=s3_object.bucket_name,
            prefix='prefix/',
            prefix_filter_fn=partial(
                S3DatasetHandler.filter_hidden_prefixes_by_dataset_content_and_load_type,
                dataset_response_full_load['attributes']["content_type"],
                dataset_response_full_load['attributes']["load_type"],
                "prefix/",
                True,
                None,
            )
        )

        filtered = [x['Key'] for x in filtered]
        assert(len(filtered) == 1) #todo specify a,b,c and nulls [from object_summaries_on_s3 magic weirdness]

    def test_skip_latest_folders_and_files_incremental_load(
            self, monkeypatch, dataset_response_incremental_load, file_service, object_summaries_on_s3
    ):
        s3_resource = boto3.resource('s3')
        s3_object = object_summaries_on_s3[0]  # 'prefix/as_of_date=2020-01-01/' is already registered in fixture

        paths = [
            'prefix/as_of_date=latest',
            'prefix/as_of_year_month=latest/',
            'prefix/as_of_year_month=latest',
            # NOTE: if as_of_date is a partition it will be top level
            'prefix/as_of_date=2021-03-01/c.parquet',
            'prefix/as_of_date=2021-02-01/b.parquet',
            'prefix/as_of_date=2021-01-01/a.parquet',
        ]
        for path in paths:
            s3_resource.Bucket(
                s3_object.bucket_name
            ).copy(
                CopySource={
                    'Bucket': s3_object.bucket_name,
                    'Key': s3_object.key
                },
                Key=path
            )

        file_service.stream_handlers['s3'].list_of_s3_files = MagicMock()
        list(file_service.get_files_from_dataset(
            dataset=dataset_response_incremental_load,
        ))

        filtered = file_service.stream_handlers['s3'].get_s3_list_filter(
            s3_resource,
            absolute_path=False,
            bucket_name=s3_object.bucket_name,
            prefix='prefix/',
            prefix_filter_fn=partial(
                S3DatasetHandler.filter_hidden_prefixes_by_dataset_content_and_load_type,
                dataset_response_incremental_load['attributes']["content_type"],
                dataset_response_incremental_load['attributes']["load_type"],
                "prefix/",
                True,
                None,
            )
        )

        filtered = [x['Key'] for x in filtered]
        assert len(filtered) == 4 #todo specify a,b,c and nulls [from object_summaries_on_s3 magic weirdness]

    @pytest.mark.parametrize(
        'query_partitions,expected', [
            [
                [
                    {
                        'partition': 'as_of_date',
                        'operator': '=',
                        'value': '2021-02-01'
                    }
                ],
                ['prefix/as_of_date=2021-02-01/b.parquet'],
            ],

            [
                [
                    {
                        'partition': 'as_of_date',
                        'operator': '>=',
                        'value': '2021-02-01'
                    }
                ],
                ['prefix/as_of_date=2021-03-01/c.parquet', 'prefix/as_of_date=2021-02-01/b.parquet'],
            ],

            [
                [
                    {
                        'partition': 'as_of_date',
                        'operator': '>',
                        'value': '2021-02-01'
                    }
                ],
                ['prefix/as_of_date=2021-03-01/c.parquet'],
            ],

            [
                [
                    {
                        'partition': 'as_of_date',
                        'operator': '<',
                        'value': '2021-02-01'
                    }
                ],
                ['prefix/as_of_date=2021-01-01/a.parquet', 'prefix/as_of_date=2020-01-01/nulls_and_unicode.parquet'],
            ],

            [
                [
                    {
                        'partition': 'as_of_date',
                        'operator': '<=',
                        'value': '2021-02-01'
                    }
                ],
                ['prefix/as_of_date=2021-02-01/b.parquet', 'prefix/as_of_date=2021-01-01/a.parquet', 'prefix/as_of_date=2020-01-01/nulls_and_unicode.parquet'],
            ],

            # Empty query_partitions should return all.
            [
                [],
                ['prefix/as_of_date=2021-03-01/c.parquet', 'prefix/as_of_date=2021-02-01/b.parquet', 'prefix/as_of_date=2021-01-01/a.parquet', 'prefix/as_of_date=2020-01-01/nulls_and_unicode.parquet'],
            ],

            # Non-as_of query does not perform filtering on the common prefix.
            [
                [
                    {
                        'partition': 'country',
                        'operator': '=',
                        'value': 'US'
                    }
                ],
                ['prefix/as_of_date=2021-03-01/c.parquet', 'prefix/as_of_date=2021-02-01/b.parquet',
                 'prefix/as_of_date=2021-01-01/a.parquet', 'prefix/as_of_date=2020-01-01/nulls_and_unicode.parquet'],
            ],
        ],
    )
    def test_query_partition_as_of_equals_to_common_prefix_incremental_load(
            self, monkeypatch, dataset_response_incremental_load, file_service, object_summaries_on_s3,
            query_partitions, expected
    ):
        s3_resource = boto3.resource('s3')
        s3_object = object_summaries_on_s3[0]  # 'prefix/as_of_date=2020-01-01/' is already registered in fixture

        paths = [
            'prefix/as_of_date=latest',
            'prefix/as_of_year_month=latest/',
            'prefix/as_of_year_month=latest',
            # NOTE: if as_of_date is a partition it will be top level
            'prefix/as_of_date=2021-03-01/c.parquet',
            'prefix/as_of_date=2021-02-01/b.parquet',
            'prefix/as_of_date=2021-01-01/a.parquet',
        ]
        for path in paths:
            s3_resource.Bucket(
                s3_object.bucket_name
            ).copy(
                CopySource={
                    'Bucket': s3_object.bucket_name,
                    'Key': s3_object.key
                },
                Key=path
            )

        file_service.stream_handlers['s3'].list_of_s3_files = MagicMock()
        list(file_service.get_files_from_dataset(
            dataset=dataset_response_incremental_load,
        ))

        filtered = file_service.stream_handlers['s3'].get_s3_list_filter(
            s3_resource,
            absolute_path=False,
            bucket_name=s3_object.bucket_name,
            prefix='prefix/',
            prefix_filter_fn=partial(
                S3DatasetHandler.filter_hidden_prefixes_by_dataset_content_and_load_type,
                dataset_response_incremental_load['attributes']["content_type"],
                dataset_response_incremental_load['attributes']["load_type"],
                "prefix/",
                True,
                query_partitions,
            )
        )

        filtered = [x['Key'] for x in filtered]
        assert filtered == expected

    def test_skip_hadoop_files(
            self, dataset_response, file_service, aws_s3
    ):
        s3_resource = boto3.resource('s3')
        bucket = s3_resource.create_bucket(Bucket='bucket', CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'},)  # noqa
        s3_resource.Object('bucket', 'prefix/_SUCCESS').put(
            Body=b'NOOP'
        )

        files = list(file_service.get_files_from_dataset(
            dataset=dataset_response,
            skip_special_hadoop_files=True,
        ))

        assert len(files) == 0

    def test_filters_zero_sized_files(
            self, dataset_response, file_service, aws_s3
    ):
        s3_resource = boto3.resource('s3')
        bucket = s3_resource.create_bucket(Bucket='bucket', CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'},)  # noqa
        s3_resource.Object('bucket', 'prefix/file.parquet').put(
            Body=b''
        )

        files = list(file_service.get_files_from_dataset(
            dataset=dataset_response,
            skip_special_hadoop_files=True,
        ))

        assert len(files) == 0

    @classmethod
    def create_object(cls, s3_resource, bucket, name):
        s3_resource.Object(bucket.name, name).put(Body=b'NOOP')

    def test_load_type_none_returns_data_from_all_as_of_dates(
            self, dataset_response, file_service, aws_s3
    ):
        dataset_response['attributes']['load_type'] = 'Incremental Load'

        s3_resource = boto3.resource('s3')
        bucket = s3_resource.create_bucket(Bucket='bucket', CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'},)  # noqa
        _create_object = partial(self.create_object, s3_resource, bucket)

        _create_object('prefix/as_of_date=2020-01-01/file')
        _create_object('prefix/as_of_date=2020-01-02/file')
        _create_object('prefix/as_of_date=2020-01-03/file')

        files = list(file_service.get_files_from_dataset(
            dataset=dataset_response,
            skip_hidden_files=True,
        ))

        assert len(files) == 3

    def test_load_type_incremental_returns_data_from_all_as_of_dates(
            self, dataset_response, file_service, aws_s3
    ):
        dataset_response['attributes']['load_type'] = 'Incremental Load'

        s3_resource = boto3.resource('s3')
        bucket = s3_resource.create_bucket(Bucket='bucket', CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'},)  # noqa
        _create_object = partial(self.create_object, s3_resource, bucket)

        _create_object('prefix/as_of_date=2020-01-01/file')
        _create_object('prefix/as_of_date=2020-01-02/file')
        _create_object('prefix/as_of_date=2020-01-03/file')

        files = list(file_service.get_files_from_dataset(
            dataset=dataset_response,
            skip_hidden_files=True,
        ))

        assert len(files) == 3

    def test_load_type_full_returns_data_from_most_recent_as_of_date(
            self, dataset_response, file_service, aws_s3
    ):
        dataset_response['attributes']['load_type'] = 'Full Load'

        s3_resource = boto3.resource('s3')
        bucket = s3_resource.create_bucket(Bucket='bucket', CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'},)  # noqa
        _create_object = partial(self.create_object, s3_resource, bucket)

        _create_object('prefix/as_of_date=2020-01-03/file1')
        _create_object('prefix/as_of_date=2020-01-03/file2')

        files = list(file_service.get_files_from_dataset(
            dataset=dataset_response,
            skip_hidden_files=True,
        ))

        assert [
                   f.path for f in files
               ] == [
                   'prefix/as_of_date=2020-01-03/file1',
                   'prefix/as_of_date=2020-01-03/file2'
               ]

    def test_load_type_full_but_zero_paths_returns_empty(
            self, dataset_response, file_service, aws_s3
    ):
        dataset_response['attributes']['load_type'] = 'Full Load'

        s3_resource = boto3.resource('s3')
        bucket = s3_resource.create_bucket(Bucket='bucket', CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'},)  # noqa
        _create_object = partial(self.create_object, s3_resource, bucket)

        # Create a directory but zero files.
        _create_object('prefix')

        files = list(file_service.get_files_from_dataset(
            dataset=dataset_response,
            skip_hidden_files=True,
        ))

        assert len(files) == 0

    def test_load_type_full_all_paths_without_as_of_date_return_paths(
            self, dataset_response, file_service, aws_s3
    ):
        dataset_response['attributes']['load_type'] = 'Full Load'

        s3_resource = boto3.resource('s3')
        bucket = s3_resource.create_bucket(Bucket='bucket', CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'},)  # noqa
        _create_object = partial(self.create_object, s3_resource, bucket)

        # Create a directory but zero files.
        _create_object('prefix/file-invalid1')
        _create_object('prefix/file-invalid2')
        _create_object('prefix/as_of_date=2021/file1')
        _create_object('prefix/as_of_date=2021/file2')

        files = list(file_service.get_files_from_dataset(
            dataset=dataset_response,
            skip_hidden_files=True,
        ))

        assert sorted([
            f.path for f in files
        ]) == sorted([
            'prefix/as_of_date=2021/file1',
            'prefix/as_of_date=2021/file2'
        ])

    def test_load_type_full_some_paths_without_as_of_date_return_paths(
            self, dataset_response, file_service, aws_s3
    ):
        dataset_response['attributes']['load_type'] = 'Full Load'

        s3_resource = boto3.resource('s3')
        bucket = s3_resource.create_bucket(Bucket='bucket', CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'},)  # noqa
        _create_object = partial(self.create_object, s3_resource, bucket)

        # Create a directory but zero files.
        _create_object('prefix/file-invalid1')
        _create_object('prefix/file-invalid2')
        # Now test with a mix, so we have some paths with as_of_dates
        # added to the list of paths without as_of_date.

        _create_object('prefix/as_of_date=2020-01-03/file1')
        _create_object('prefix/as_of_date=2020-01-03/file2')

        files = list(file_service.get_files_from_dataset(
            dataset=dataset_response,
            skip_hidden_files=True,
        ))

        # We expect to return the paths that did not have an as_of_date (as a
        # fallback behaviour so that the files are not `lost`) and return the
        # paths that contain the most recent as_of_date.
        assert sorted([
            f.path for f in files
        ]) == sorted([
            #'prefix/file-invalid1', # TODO HOW TO RETURN THIS AS WELL
            'prefix/as_of_date=2020-01-03/file1',
            'prefix/as_of_date=2020-01-03/file2',
            #'prefix/file-invalid2', # TODO HOW TO RETURN THIS AS WELL
        ])

    def test_partial_as_of_date(
            self, dataset_response_incremental_load, file_service, aws_s3
    ):
        s3_resource = boto3.resource('s3')
        bucket = s3_resource.create_bucket(Bucket='bucket', CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'},)  # noqa
        _create_object = partial(self.create_object, s3_resource, bucket)

        _create_object('prefix/as_of_date=2020-01/file')
        _create_object('prefix/as_of_date=2020-01-01/file')
        _create_object('prefix/as_of_date=2020-02/file')
        _create_object('prefix/as_of_date=2020-03/file1')

        partitionquery = [{
            'partition': 'as_of_date',
            'operator': '=',
            'value': '2020-02'
        }]

        files = list(file_service.get_files_from_dataset(
            dataset=dataset_response_incremental_load,
            skip_hidden_files=True,
            partitions=partitionquery,
        ))

        assert [
                   f.path for f in files
               ] == [
                   'prefix/as_of_date=2020-02/file'
               ]

    @pytest.mark.parametrize('path,partitionquery', [
        [path_with_as_of_date, [{
            'partition': 'as_of_date',
            'operator': '=',
            'value': '202-01-23'
        }]],
        [path_with_as_of_year_month, [{
            'partition': 'as_of_year_month',
            'operator': '=',
            'value': '202-01'
        }]],
    ])
    def test_raises_error_with_malformed_date(
            self, path: str, partitionquery: List,
    ):
        with pytest.raises(UnableToParsePartition):
            meets_partition_params(path, partitionquery)

    def test_false_when_as_of_date_is_invalid(
            self
    ):
        partitionquery = [{
            'partition': 'as_of_date',
            'operator': '=',
            'value': '2020-01-23'
        }]

        invalid_path = 'b=4/c=6/as_of_date=ABC/file.ext'

        assert not meets_partition_params(
            invalid_path,
            partitionquery
        )

    def test_load_type_full_returns_data_from_most_recent_as_of_year_month(
            self, monkeypatch, dataset_response, file_service, object_summaries_on_s3
    ):
        s3_resource = boto3.resource('s3')
        s3_object = object_summaries_on_s3[0]

        paths_in_top_level_partition = [
            'prefix/file-invalid1',
            'prefix/file-invalid2',
            'prefix/as_of_year_month=2020-03/file1',
            'prefix/as_of_year_month=2020-03/file2',
        ]

        for path in paths_in_top_level_partition:
            s3_resource.Bucket(
                s3_object.bucket_name
            ).copy(
                CopySource={
                    'Bucket': s3_object.bucket_name,
                    'Key': s3_object.key
                },
                Key=path
            )

        files = list(file_service.get_files_from_dataset(
            dataset=dataset_response,
        ))
        assert sorted([
            f.path for f in files
        ]) == sorted([
            'prefix/as_of_year_month=2020-03/file1',
            'prefix/as_of_year_month=2020-03/file2',
            # 'prefix/file-invalid1',
            # 'prefix/file-invalid2',
            # 'prefix/nulls_and_unicode.parquet'
        ])

    def test_load_type_full_some_common_prefixes_without_as_of_year_month_return_paths(
            self, monkeypatch, dataset_response, file_service, object_summaries_on_s3
    ):
        s3_resource = boto3.resource('s3')
        s3_object = object_summaries_on_s3[0]

        paths = [
            'prefix/file-invalid1',
            'prefix/file-invalid2',
            'prefix/as_of_year_month=2020-01/file',
            'prefix/as_of_year_month=2020-02/file',
            'prefix/as_of_year_month=2020-03/file1',
            'prefix/as_of_year_month=2020-03/file2',
        ]

        for path in paths:
            s3_resource.Bucket(s3_object.bucket_name).copy(
                CopySource={'Bucket': s3_object.bucket_name, 'Key': s3_object.key}, Key=path)

        files = list(file_service.get_files_from_dataset(
            dataset=dataset_response,
         ))

        assert sorted([
            f.path for f in files
        ]) == sorted([
            'prefix/as_of_year_month=2020-03/file1',
            'prefix/as_of_year_month=2020-03/file2'])


class TestOrdering:
    def test_can_order_by_path_when_no_partitions_or_metadata(self):
        result = list(FileService.order_by_latest(
            iter([
                Mock(
                    path='a/b/1', metadata={}
                ),
                Mock(
                    path='a/b/2', metadata={}
                ),
                Mock(
                    path='a/b/3', metadata={}
                ),
            ])
        ))

        assert [r.path for r in result] == [
            'a/b/3', 'a/b/2', 'a/b/1',
        ]

    def test_ordering_param(self):
        result = list(FileService.order_by_latest(
            iter([
                Mock(
                    path='a/b/1', metadata={}
                ),
                Mock(
                    path='a/b/2', metadata={}
                ),
                Mock(
                    path='a/b/3', metadata={}
                ),
            ]),
            direction='asc'
        ))

        assert [r.path for r in result] == [
            'a/b/1', 'a/b/2', 'a/b/3',
        ]

    def test_presence_of_medatadata_prioritizes(self):

        result = list(FileService.order_by_latest(
            iter([
                Mock(
                    path='a/b/1', metadata={
                        'last_modified': datetime.datetime.now()
                    }
                ),
                Mock(
                    path='a/b/2', metadata={}
                ),
            ])
        ))

        assert [r.path for r in result] == [
            'a/b/1', 'a/b/2'
        ]

    def test_can_order_by_partition_year(self):

        result = list(FileService.order_by_latest(
            iter([
                Mock(
                    path='a/Year=1', metadata={
                        'last_modified': datetime.datetime.now()
                    }
                ),
                Mock(
                    path='a/Year=2', metadata={
                        # Check ignore metadata and prioritises partition
                        'last_modified': (
                                datetime.datetime.now() -
                                datetime.timedelta(days=1)
                        )
                    }
                ),
            ])
        ))

        assert [r.path for r in result] == [
            'a/Year=2', 'a/Year=1'
        ]

    def test_can_order_by_partition_year_month_combination(self):

        result = list(FileService.order_by_latest(
            iter([
                Mock(
                    path='a/Year=1/month=1/day=1', metadata={
                        'last_modified': datetime.datetime.now()
                    }
                ),
                Mock(
                    path='a/Year=1/month=2/day=1', metadata={}
                ),
            ])
        ))

        assert [r.path for r in result] == [
            'a/Year=1/month=2/day=1', 'a/Year=1/month=1/day=1'
        ]

    def test_can_order_by_as_of_date(self):


        result = list(FileService.order_by_latest(
            iter([
                Mock(path='b/as_of_date=2000-01-01/', metadata={}),
                Mock(path='b/as_of_date=2000-01-02/', metadata={}),
            ])
        ))

        assert [r.path for r in result] == [
            'b/as_of_date=2000-01-02/', 'b/as_of_date=2000-01-01/'
        ]

    def test_can_order_by_as_of_year_month(self):

        result = list(FileService.order_by_latest(
            iter([
                Mock(path='b/as_of_year_month=2000-01/', metadata={}),
                Mock(path='b/as_of_year_month=2000-02/', metadata={}),
            ])
        ))

        assert [r.path for r in result] == [
            'b/as_of_year_month=2000-02/', 'b/as_of_year_month=2000-01/'
        ]

    def test_as_of_date_none_but_last_modified_available(self):

        result = list(FileService.order_by_latest(
            iter([
                Mock(path='b/as_of_date=2000-01-01/', metadata={}),
                Mock(path='b/as_of_date=2000-01-02/', metadata={}),
                Mock(path='b/as_of_date=None',
                     metadata={
                         'last_modified': datetime.datetime.now()
                     }),
            ])
        ))

        assert [r.path for r in result] == [
            'b/as_of_date=2000-01-02/',
            'b/as_of_date=2000-01-01/',
            'b/as_of_date=None',
        ]

    def test_as_of_year_month_none_but_last_modified_available(self):

        result = list(FileService.order_by_latest(
            iter([
                Mock(path='b/as_of_year_month=2000-01/', metadata={}),
                Mock(path='b/as_of_year_month=2000-02/', metadata={}),
                Mock(path='b/as_of_year_month=None',
                     metadata={
                         'last_modified': datetime.datetime.now()
                     }),
            ])
        ))

        assert [r.path for r in result] == [
            'b/as_of_year_month=2000-02/',
            'b/as_of_year_month=2000-01/',
            'b/as_of_year_month=None',
        ]

    def test_as_of_date_none_and_last_modified_not_available(self):

        result = list(FileService.order_by_latest(
            iter([
                Mock(path='b/as_of_date=2000-01-01/', metadata={}),
                Mock(path='b/as_of_date=2000-01-02/', metadata={}),
                Mock(path='b/as_of_date=None', metadata={}),
            ])
        ))

        assert [r.path for r in result] == [
            'b/as_of_date=2000-01-02/',
            'b/as_of_date=2000-01-01/',
            'b/as_of_date=None'
        ]

    def test_as_of_year_month_none_and_last_modified_not_available(self):

        result = list(FileService.order_by_latest(
            iter([
                Mock(path='b/as_of_year_month=2000-01/', metadata={}),
                Mock(path='b/as_of_year_month=2000-02/', metadata={}),
                Mock(path='b/as_of_year_month=None', metadata={}),
            ])
        ))

        assert [r.path for r in result] == [
            'b/as_of_year_month=2000-02/',
            'b/as_of_year_month=2000-01/',
            'b/as_of_year_month=None'
        ]

    def test_as_of_date_is_latest(self):

        result = list(FileService.order_by_latest(
            iter([
                Mock(path='b/as_of_date=2000-01-01/', metadata={}),
                Mock(path='b/as_of_date=2000-01-02/', metadata={}),
                Mock(path='b/as_of_date=latest', metadata={}),
                Mock(path='b/as_of_date=latest', metadata={
                    'last_modified': datetime.datetime.now()
                }),
            ])
        ))

        assert [r.path for r in result] == [
            'b/as_of_date=2000-01-02/',
            'b/as_of_date=2000-01-01/',
            'b/as_of_date=latest',
            'b/as_of_date=latest',
        ]

    def test_sort_as_of_date_with_iso8601(self):

        time = datetime.datetime.now()
        time_plus_1h = (time + datetime.timedelta(hours=1))

        result = list(FileService.order_by_latest(
            iter(
                [
                    Mock(
                        temp_identifier='time',
                        path=f'b/as_of_date={time.isoformat()}/',
                        metadata={
                            'last_modified': time
                        }
                    ),
                    Mock(
                        temp_identifier='time+1hour',
                        path=f'b/as_of_date={time_plus_1h.isoformat()}/',
                        metadata={
                            'last_modified': time_plus_1h
                        }
                    ),
                ]
            )
        ))

        assert [r.temp_identifier for r in result] == [
            'time+1hour', 'time'
        ]

    def test_partitions_response_sorted(
            self, dlc_service, object_summaries_on_s3, platform_app_blueprint, dataset_response
    ):
        # In order to test if the response values from
        # get_partitions_from_dataset are sorted -
        # we need to mock the all_split generator variable
        # via get_files_from_dataset and _get_partitions_in_filepath,
        # with the latter being a classmethod.
        service = FileService(
            dlc_service=dlc_service,
        )

        Temp = namedtuple('Temp', ['path'])

        service.get_files_from_dataset = Mock(
            return_value=iter([
                Temp(path='as_of_date=2019-08-18/type=full'),
                Temp(path='as_of_date=2019-08-17/type=full/country=UK'),
                Temp(path='as_of_date=2019-08-19/type=full/')
            ])
        )

        parts = service.get_partitions_from_dataset(
            dataset_response
        )

        assert parts['as_of_date'] == [
            '2019-08-17', '2019-08-18', '2019-08-19',
        ]


@mock_sts
class TestS3Caching:

    def test_get_files_caches_basic(
            self, dlc_service, object_summaries_on_s3, platform_app_client_with_handler,
            dataset_response,
    ):

        service = FileService(
            dlc_service=dlc_service,
        )

        files = list(
            service.get_files_from_dataset(
                dataset=dataset_response,
            )
        )
        assert len(files) == 1
        assert files[0].path == 'prefix/as_of_date=2020-01-01/nulls_and_unicode.parquet'

        # TODO scott needs a lot more testing.
