#
# Copyright (C) 2019 IHS Markit.
# All Rights Reserved
#
import bz2
import datetime
import gzip
import lzma
import os
import io
import string
from typing import Iterator
import itertools

import boto3
import hypothesis
import hypothesis.extra.pandas as hpd
import hypothesis.strategies as st
import pandas.testing
import pyarrow
import pytest
from freezegun import freeze_time
from hypothesis import settings
from moto import mock_s3

from .conftest import IPC_STREAM_END
from ..services.arrow_service.exceptions import (
    NonCsvFilesInDataset
)
from ..services.arrow_service.handlers.csv import CsvHandler
from ..adapters.s3_io_adapters import ServiceIO, S3File
from ..services.exceptions import SchemaMismatchException


@mock_s3
def s3_object_from_file(io):

    with freeze_time('2020-01-01T00:00:00Z'):
        s3_resource = boto3.resource('s3')
        bucket = s3_resource.create_bucket(Bucket='bucket', CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'},)

        s3_resource.Object('bucket', f'prefix/{io.name}').put(
            Body=io.read()
        )

    page_iterator = s3_resource.meta.client.get_paginator(
        'list_objects_v2'
    ).paginate(Bucket=bucket.name)

    for page in page_iterator:
        for key in page['Contents']:
            return S3File(
                key_dict=key,
                bucket_name=bucket.name,
                get_object=s3_resource.meta.client.get_object
            )


class TestCsvHandlerBasic:

    @staticmethod
    def yield_s3_object_from_path(
        path='string_int.csv'
    ) -> Iterator[ServiceIO]:

        # path depends on whether running from top-level or not (PyCharm debug vs. pytest command line)
        path = os.path.join(f"{path}")
        if not os.path.exists(path):
            path = os.path.join(f"{os.getcwd()}/data/csv_test/{path}")

        with open(path, 'rb') as f:
            yield s3_object_from_file(f)

    @staticmethod
    def to_s3_object(
            csv: str,
            filename: str,
    ) -> Iterator[ServiceIO]:
        s3_resource = boto3.resource('s3')
        bucket = s3_resource.create_bucket(Bucket='bucket', CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'},)
        # Minimal compression for speed.
        compression_level = 1

        if filename.endswith('gz'):
            data = gzip.compress(
                csv.encode('utf-8'),
                compresslevel=compression_level
            )
            hypothesis.event('gz compression')
        elif filename.endswith('bz2'):
            data = bz2.compress(
                csv.encode('utf-8'),
                compresslevel=compression_level
            )
            hypothesis.event('bz2 compression')
        elif filename.endswith('xz'):
            data = lzma.compress(csv.encode('utf-8'))
            hypothesis.event('xz compression')
        else:
            hypothesis.event('no compression')
            data = csv.encode('utf-8')

        s3_resource.Object(bucket.name, f'prefix/{filename}').put(
            Body=data
        )

        page_iterator = s3_resource.meta.client.get_paginator(
            'list_objects_v2'
        ).paginate(Bucket=bucket.name)

        for page in page_iterator:
            for key in page['Contents']:
                yield S3File(
                    key_dict=key,
                    bucket_name=bucket.name,
                    get_object=s3_resource.meta.client.get_object
                )

    @staticmethod
    def create_reader(chunk_size, num_files, s3_files_gen, nrows=None):
        s3_files = iter([])
        for _ in range(0, num_files):
            s3_files = itertools.chain(s3_files, s3_files_gen())

        handler = CsvHandler(
            s3_files,
            chunk_size=chunk_size
        )
        stream_of_bytes = handler.handle(nrows=nrows)
        ipc_stream = b''.join(stream_of_bytes)
        return pyarrow.RecordBatchStreamReader(ipc_stream)

    text_strat = st.one_of(
        st.none(),
        st.text(
            alphabet=string.digits + string.ascii_letters + string.punctuation,
            min_size=1
        ),
    )
    df_strat = hpd.data_frames(
        index=hpd.range_indexes(),
        columns=[
            hpd.column('bools', elements=st.booleans()),
            hpd.column('strs', elements=text_strat),
            hpd.column('ints', elements=st.integers(
                min_value=-1000, max_value=1000
            )),
            hpd.column('floats', elements=st.floats()),
            hpd.column('dates', elements=st.dates()),
            hpd.column('datetimes', elements=st.datetimes(
                min_value=datetime.datetime(year=2000, month=1, day=1),
                max_value=datetime.datetime(year=2020, month=1, day=1)
            )),
            hpd.column('timedeltas', elements=st.timedeltas(
                min_value=datetime.timedelta(days=0),
                max_value=datetime.timedelta(days=1),
            )),
            hpd.column('times', elements=st.times()),
        ]
    )

    path_strat = st.text(
        alphabet=string.digits + string.ascii_letters + string.punctuation
    )
    filename_strat = st.text(
        alphabet=string.digits + string.ascii_letters + string.punctuation,
        min_size=1,
    )
    # Not testing .zip compression as there does not seem to be an easy way
    # to create them in memory in Python.
    compression_file_extension_strat = st.shared(st.sampled_from(
        ['gz', 'bz2', 'xz']
    ))

    @settings(deadline=300)
    @hypothesis.given(
        filename=st.tuples(
            st.text(alphabet=string.ascii_lowercase, min_size=1),
            compression_file_extension_strat,
        ).map(lambda x: f'{x[0]}.csv.{x[1]}'),
        # Only a header row followed by an empty row (which we expect to be
        # skipped).
        csv_header_only=st.lists(
            st.text(string.ascii_lowercase, min_size=1),
            min_size=1,
        ).map(lambda x: ','.join(x) + '\r\n'),
    )
    def test_empty_rows_csv(self, filename, csv_header_only):
        with mock_s3() as _:
            def s3_files():
                return self.to_s3_object(
                    csv=csv_header_only,
                    filename=filename,
                )
            num_files = 1
            reader = self.create_reader(100, num_files, s3_files)

            result_df = reader.read_pandas()

            assert result_df.shape[1] > 0, \
                'Must have column headers'
            assert result_df.shape[0] == 0, \
                'Must have zero rows (header is not included in row count)'

    @hypothesis.example(path='/path/file', expected=None)
    @hypothesis.example(path='/path/file.csv', expected='csv')
    @hypothesis.example(path='/path/file.csv.gz', expected='gz')
    @hypothesis.example(path='/path/file.csv.bz2', expected='bz2')
    @hypothesis.example(path='/path/file.csv.zip', expected='zip')
    @hypothesis.example(path='/path/file.csv.xz', expected='xz')
    @hypothesis.given(
        path=st.tuples(
            path_strat,
            filename_strat,
            compression_file_extension_strat
        ).map(lambda x: f'{x[0]}/{x[1]}.csv.{x[2]}'),
        expected=compression_file_extension_strat,
    )
    def test_extract_file_extension(self, path, expected):
        result = CsvHandler._extract_file_extension(path=path)
        assert result == expected

    @hypothesis.given(
        input_df=df_strat,
        filename=st.tuples(
            st.text(alphabet=string.ascii_lowercase, min_size=1),
            compression_file_extension_strat,
        ).map(lambda x: f'{x[0]}.csv.{x[1]}'),
        chunk_size=st.integers(min_value=1, max_value=1000),
    )
    def test_with_single_random_file(self,
                                     input_df: pandas.DataFrame,
                                     filename: str,
                                     chunk_size: int):
        # If we create the mock s3 via a fixture, then it is a singleton
        # shared across all of the Hypothesis test examples run by this
        # example. This is not what we want as it means state (the files
        # added to S3) are shared between test runs.
        with mock_s3() as _:
            csv = input_df.to_csv(
                # We do not need the row number added to the first column of
                # the .csv.
                index=False,
            )

            def s3_files():
                return self.to_s3_object(
                    csv=csv,
                    filename=filename,
                )
            num_files = 1
            reader = self.create_reader(chunk_size, num_files, s3_files)

            result_df = reader.read_pandas()

            assert result_df.shape == input_df.shape, \
                'Must have the same number of rows (header is not ' \
                'included in row count)'
            assert result_df.to_csv(index=False) == csv, \
                'When the resulting DataFrame is turned back into a csv, ' \
                'it should be identical to the original input'

    def test_with_single_file(self, aws_s3, request):
        s3_files = self.yield_s3_object_from_path()
        handler = CsvHandler(s3_files, chunk_size=1000)
        stream_of_bytes = handler.handle()
        ipc_stream = b''.join(stream_of_bytes)
        reader = pyarrow.RecordBatchStreamReader(ipc_stream)
        df = reader.read_pandas()

        assert ipc_stream[-8:] == IPC_STREAM_END
        assert df.shape == (3, 2), \
            'Must have 3 rows (header is not included in row count)'
        expected = pandas.DataFrame(
            {
                'foo': ['a', 'b', 'c'],
                'bar': ['0', '1', '2']
            }
        )
        pandas.testing.assert_frame_equal(df, expected)

    def test_joining_n_files(self, aws_s3, request):
        def s3_files():
            return self.yield_s3_object_from_path()
        chunk_size = 1000
        num_files = 3
        reader = self.create_reader(chunk_size, num_files, s3_files)

        df = reader.read_pandas()

        assert df.shape == (3 * num_files, 2), \
            'Must have 3*n rows (header is not included in row count)'
        expected = pandas.DataFrame(
            {
                'foo': ['a', 'b', 'c'] * num_files,
                'bar': ['0', '1', '2'] * num_files
            }
        )
        pandas.testing.assert_frame_equal(df, expected)

    def test_joining_n_files_benchmark(self, aws_s3, request):
        def s3_files():
            return self.yield_s3_object_from_path()
        chunk_size = 1000
        num_files = 3
        reader = self.create_reader(chunk_size, num_files, s3_files)

        df = reader.read_pandas()

        assert df.shape == (3 * num_files, 2), \
            'Must have 3*n rows (header is not included in row count)'
        expected = pandas.DataFrame(
            {
                'foo': ['a', 'b', 'c'] * num_files,
                'bar': ['0', '1', '2'] * num_files
            }
        )
        pandas.testing.assert_frame_equal(df, expected)

    def test_joining_n_files_nrows_less_than_total(self, aws_s3, request):
        def s3_files():
            return self.yield_s3_object_from_path()
        chunk_size = 1000
        num_files = 100
        nrows = 10
        reader = self.create_reader(chunk_size, num_files, s3_files, nrows)

        df = reader.read_pandas()

        assert df.shape == (nrows, 2), f'Must have {nrows} rows'

    def test_joining_n_files_nrows_more_than_total(self, aws_s3, request):
        def s3_files():
            return self.yield_s3_object_from_path()
        chunk_size = 1000
        num_files = 100
        nrows = 100000000
        reader = self.create_reader(chunk_size, num_files, s3_files, nrows)

        df = reader.read_pandas()

        assert df.shape == (3 * num_files, 2), (
            'Must have 3*n rows (header is not included in row count)'
        )

    def test_joining_single_file_nrow(self, aws_s3, request):
        def s3_files():
            return self.yield_s3_object_from_path()
        chunk_size = 1000
        num_files = 100
        nrows = 1
        reader = self.create_reader(chunk_size, num_files, s3_files, nrows)

        df = reader.read_pandas()

        assert df.shape == (1, 2), \
            'Must have 1 rows (header is not included in row count)'
        expected = pandas.DataFrame(
            {
                'foo': ['a'],
                'bar': ['0']
            }
        )
        pandas.testing.assert_frame_equal(df, expected)

    def test_raise_when_initial_file_is_parquet_in_csv_dataset(self):
        file_1 = io.BytesIO(b'a,b,c\n1,2,3')
        file_1.path = '1.parquet'
        file_1.size = 1

        with pytest.raises(NonCsvFilesInDataset) as exc:
            CsvHandler(iter([file_1]))

        assert exc.match('Non csv file found in dataset. Path: 1.parquet')

    def test_raise_when_second_file_is_parquet_in_csv_dataset(self):
        file_1 = io.BytesIO(b'a,b,c\n1,2,3')
        file_1.path = '1.csv'
        file_1.size = 1

        file_2 = io.BytesIO(b'a,b,c\n1,2,3')
        file_2.path = '2.parquet'
        file_2.size = 1

        with pytest.raises(NonCsvFilesInDataset) as exc:
            stream = CsvHandler(iter([file_1, file_2])).handle()

            chunk_output = b''

            while True:
                try:
                    chunk_output += next(stream)
                except SchemaMismatchException:
                    break

        assert exc.match(
            'Non csv file found in dataset. Path: 2.parquet')

    def test_skips_file_when_subsequent_file_is_zero_bytes(self):
        file_1 = io.BytesIO(b'a,b,c\n1,2,3')
        file_1.path = '1.csv'
        file_1.size = 1

        file_2 = io.BytesIO(b'a,b,c\n1,2,3')
        file_2.path = '2.csv'
        file_2.size = 0

        stream = CsvHandler(iter([file_1, file_2])).handle()

        ipc_stream = b''.join(stream)

        reader = pyarrow.RecordBatchStreamReader(ipc_stream)
        df = reader.read_pandas()
        assert df.shape == (1, 3), 'Must only have the number of rows from ' \
                                   'one file (where the metadata is > 0 ' \
                                   'bytes), not rows from both files.'

    def test_skips_file_when_first_file_is_zero_bytes(self):
        file_1 = io.BytesIO(b'a,b,c\n1,2,3')
        file_1.path = '1.csv'
        file_1.size = 0

        file_2 = io.BytesIO(b'a,b,c\n1,2,3')
        file_2.path = '2.csv'
        file_2.size = 1

        stream = CsvHandler(iter([file_1, file_2])).handle()

        ipc_stream = b''.join(stream)

        reader = pyarrow.RecordBatchStreamReader(ipc_stream)
        df = reader.read_pandas()
        assert df.shape == (1, 3), 'Must only have the number of rows from ' \
                                   'one file (where the metadata is > 0 ' \
                                   'bytes), not rows from both files.'

    def test_additive_schema(self):
        file_1 = io.BytesIO(b'a\n1a')
        file_1.path = '1.csv'
        file_1.size = 1

        file_2 = io.BytesIO(b'a,b\n2a,2b')
        file_2.path = '2.csv'
        file_2.size = 1

        file_3 = io.BytesIO(b'a,b,c\n3a,3b,3c')
        file_3.path = '3.csv'
        file_3.size = 1

        stream = CsvHandler(
            iter([file_1, file_2, file_3]),
        ).handle()

        ipc_stream = b''.join(stream)
        reader = pyarrow.RecordBatchStreamReader(ipc_stream)

        df = reader.read_pandas()

        expected = pandas.DataFrame(
            {
                'a': ['1a', '2a', '3a'],
                'b': [None, '2b', '3b'],
                'c': [None, None, '3c'],
            }
        )
        pandas.testing.assert_frame_equal(df, expected)

    def test_schema_mismatch_exception(self):
        file_1 = io.BytesIO(b'aaa,bbb\n1,2')
        file_1.path = 's3://some-path1.csv'
        file_1.size = 1

        # Column names are non-additive
        file_2 = io.BytesIO(b'ddd,eee\n1,2')
        file_2.path = 's3://some-path2.csv'
        file_2.size = 1

        stream = CsvHandler(
            iter([file_1, file_2]),
        ).handle()

        with pytest.raises(SchemaMismatchException) as exc:
            list(stream)

        expected_message = \
            'Tried to process a file with a schema that does not ' \
            'match the schema of the latest. We ' \
            'require that all .csv files have an additive ' \
            'schema.' \
            "\n\nLatest file's schema:" \
            "\n\n['ddd', 'eee']" \
            "\n\nLatest file's path:" \
            '\n\ns3://some-path2.csv' \
            "\n\nCurrent file's schema:" \
            "\n\n['aaa', 'bbb']" \
            "\n\nCurrent file's path:" \
            '\n\ns3://some-path1.csv'

        assert exc.value.details == expected_message
