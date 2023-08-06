#
# Copyright (C) 2019 IHS Markit.
# All Rights Reserved
#
import os
import tempfile
from unittest import mock
from unittest.mock import MagicMock

import boto3
import pytest
import random
import numpy
import pandas
import pyarrow
import pyarrow.parquet as pq
from freezegun import freeze_time
from pyarrow import ArrowException
from pyarrow.lib import ArrowNotImplementedError

from .conftest import IPC_STREAM_END
from ..services.arrow_service.exceptions import NonParquetFilesInDataset
from ..services.exceptions import ServiceException, SchemaMismatchException
from ..services.arrow_service import NoFilesInDataset
from ..services.arrow_service.handlers.parquet import ParquetHandler
from ..adapters.s3_io_adapters import S3File


@pytest.fixture
def object_summaries(aws_s3, request):
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

        s3_resource.Object('bucket', path).put(
            Body=file_data
        )

    yield [f for f in bucket.objects.all()]


@pytest.fixture
def files(object_summaries):
    s3_files = []
    for obj_sum in object_summaries:
        s3_file = S3File(
            key_dict={
                'Key': obj_sum.key,
                'ETag': obj_sum.e_tag,
                'LastModified': obj_sum.last_modified,
                'Size': obj_sum.size
            },
            get_object=obj_sum.meta.client.get_object,
            bucket_name=obj_sum.bucket_name,
        )

        s3_files.append(s3_file)

    return iter(s3_files)


class TestParquetHandlerBasic:
    # NOTE: install pyarrow whl in repo to run tests locally!

    @pytest.mark.parametrize(
        'object_summaries',
        ['nulls_and_unicode.parquet'],
        indirect=True
    )
    def test_with_single_file(self, files):
        first_file = next(files)
        ipc_stream = b''.join(
            ParquetHandler(iter([first_file])).handle()
        )

        reader = pyarrow.RecordBatchStreamReader(ipc_stream)
        dataframe = reader.read_pandas()
        assert ipc_stream[-8:] == IPC_STREAM_END
        assert dataframe.shape == (1000, 13)

    def test_with_not_null_schema(self):
        # Regression test for DL-3053
        schema = pyarrow.schema([
            # By default nullable is true
            pyarrow.field('s', 'string', nullable=False)]
        )

        batch_array = pyarrow.array(['abc', 'åbc'])
        table = pyarrow.Table.from_arrays([batch_array], schema=schema)

        expected_df = table.to_pandas()

        def _parquet_file():
            with tempfile.NamedTemporaryFile() as f:
                expected_df.to_parquet(f.name)
                return pq.ParquetFile(f.name)

        input1 = MagicMock()
        input1.to_parquet_file = _parquet_file
        input1.backend_type = 'some-backend_type'
        input1.path = 's3://some-path.parquet'
        input1.metadata = {'size': 1}
        input1.size = 1

        stream = ParquetHandler(iter([input1])).handle()

        ipc_stream = b''.join(stream)

        reader = pyarrow.RecordBatchStreamReader(ipc_stream)
        dataframe = reader.read_pandas()

        assert ipc_stream[-8:] == IPC_STREAM_END
        assert dataframe.shape == (2, 1)

    def test_raises_exception_for_schema_mismatch(self, files):
        """
        Assert that the stream from the handler still has a
        termination marker even if there's an exception
        """
        df1 = pandas.DataFrame({'a': [1]})

        def _parquet_file1():
            with tempfile.NamedTemporaryFile() as f:
                df1.to_parquet(f.name)
                return pq.ParquetFile(f.name)

        input1 = MagicMock()
        input1.to_parquet_file = _parquet_file1
        input1.backend_type = 'some-backend_type'
        input1.path = 's3://some-path.parquet'
        input1.metadata = {'size': 1}
        input1.size = 1

        df2 = pandas.DataFrame({'b': ['a']})

        def _parquet_file2():
            with tempfile.NamedTemporaryFile() as f:
                df2.to_parquet(f.name)
                return pq.ParquetFile(f.name)

        input2 = MagicMock()
        input2.to_parquet_file = _parquet_file2
        input2.backend_type = 'some-backend_type'
        input2.path = 's3://some-path.parquet'
        input2.metadata = {'size': 1}
        input2.size = 1

        stream = ParquetHandler(
            iter([input1, input2])
        ).handle()

        chunk_output = b''

        while True:
            try:
                chunk_output += next(stream)
            except SchemaMismatchException:
                break

        assert chunk_output[-8:] == IPC_STREAM_END

    def test_raise_exception_for_transposed_columns(self, files):
        """
        Assert that the stream from the handler still has a
        termination marker even if there's an exception
        """

        df1 = pandas.DataFrame(data=[['aaa', 1]], columns=['a', 'b'])

        def _parquet_file1():
            with tempfile.NamedTemporaryFile() as f:
                df1.to_parquet(f.name)
                return pq.ParquetFile(f.name)

        input1 = MagicMock()
        input1.to_parquet_file = _parquet_file1
        input1.backend_type = 'some-backend_type'
        input1.path = 's3://some-path.parquet'
        input1.metadata = {'size': 1}
        input1.size = 1

        # create a new file with columns transposed.
        df2 = pandas.DataFrame(data=[[2, 'bbb']], columns=['b', 'a'])

        def _parquet_file2():
            with tempfile.NamedTemporaryFile() as f:
                df2.to_parquet(f.name)
                return pq.ParquetFile(f.name)

        input2 = MagicMock()
        input2.to_parquet_file = _parquet_file2
        input2.backend_type = 'some-backend_type'
        input2.path = 's3://some-path.parquet'
        input2.metadata = {'size': 1}
        input2.size = 1

        stream = ParquetHandler(
            iter([input1, input2])
        ).handle()

        with pytest.raises(SchemaMismatchException) as exc:
            list(stream)
        assert exc.value.details.startswith(
            'Tried to process a file with a schema that does not match '
        )

    def test_raise_exception_for_renamed_columns(self, monkeypatch, files):
        """
        Assert that the stream from the handler still has a
        termination marker even if there's an exception
        """
        df1 = pandas.DataFrame(data=[['aaa', 'bbb']], columns=['a', 'b'])

        # create a new file with last column name capitalised.
        df2 = pandas.DataFrame(data=[['ccc', 'ddd']], columns=['a', 'B'])

        def _parquet_file1():
            with tempfile.NamedTemporaryFile() as f:
                df1.to_parquet(f.name)
                return pq.ParquetFile(f.name)

        input1 = MagicMock()
        input1.to_parquet_file = _parquet_file1
        input1.backend_type = 'some-backend_type'
        input1.path = 's3://some-path1.parquet'
        input1.metadata = {'size': 1}
        input1.size = 1

        def parquet_file2():
            with tempfile.NamedTemporaryFile() as f:
                df2.to_parquet(f.name)
                return pq.ParquetFile(f.name)

        input2 = MagicMock()
        input2.to_parquet_file = parquet_file2
        input2.backend_type = 'some-backend_type'
        input2.path = 's3://some-path2.parquet'
        input2.metadata = {'size': 1}
        input2.size = 1

        stream = ParquetHandler(iter([
            input1, input2
        ])).handle()

        with pytest.raises(SchemaMismatchException) as exc:
            list(stream)

        expected_message = \
            'Tried to process a file with a schema that does not ' \
            'match the schema of the latest. We ' \
            'require that all .parquet files have an additive ' \
            'schema.' \
            "\n\nLatest file's schema:" \
            "\n\na: string" \
            "\nb: string" \
            "\n\nLatest file's path:" \
            '\n\ns3://some-path1.parquet' \
            "\n\nCurrent file's schema:" \
            "\n\na: string" \
            "\nB: string" \
            "\n\nCurrent file's path:" \
            '\n\ns3://some-path2.parquet'

        assert exc.value.details == expected_message, \
            f'Returned message from the exception:\n{exc.value.details}'

    @pytest.mark.parametrize(
        'object_summaries',
        ['nulls_and_unicode.parquet'],
        indirect=True
    )
    def test_joining_files(self, files):
        ipc_stream = b''.join(
            ParquetHandler(iter(list(files) * 3), close_s3_files=False).
                handle()
        )

        reader = pyarrow.RecordBatchStreamReader(ipc_stream)
        dataframe = reader.read_pandas()
        assert dataframe.shape == (3000, 13)

    @pytest.mark.parametrize(
        'object_summaries',
        ['nulls_and_unicode.parquet'],
        indirect=True
    )
    def test_joining_n_files_nrows_less_than_total(self, files):
        ipc_stream = b''.join(
            ParquetHandler(iter(list(files) * 3), close_s3_files=False).
                handle(nrows=10)
        )

        reader = pyarrow.RecordBatchStreamReader(ipc_stream)
        dataframe = reader.read_pandas()
        assert dataframe.shape == (10, 13)

    @pytest.mark.parametrize(
        'object_summaries',
        ['nulls_and_unicode.parquet'],
        indirect=True
    )
    def test_joining_n_files_nrows_greater_than_total(self, files):
        ipc_stream = b''.join(
            ParquetHandler(iter(list(files) * 3), close_s3_files=False).
                handle(nrows=10000)
        )

        reader = pyarrow.RecordBatchStreamReader(ipc_stream)
        dataframe = reader.read_pandas()
        assert dataframe.shape == (3000, 13)

    @pytest.mark.parametrize(
        'object_summaries',
        ['nulls_and_unicode.parquet'],
        indirect=True
    )
    def test_nrows_greater_than_total(self, files):
        ipc_stream = b''.join(
            ParquetHandler(files).handle(nrows=10000)
        )

        reader = pyarrow.RecordBatchStreamReader(ipc_stream)
        dataframe = reader.read_pandas()
        assert dataframe.shape == (1000, 13)

    @pytest.mark.parametrize(
        'object_summaries',
        ['nulls_and_unicode.parquet'],
        indirect=True
    )
    def test_nrows_less_than_total(self, files):
        ipc_stream = b''.join(
            ParquetHandler(files).handle(nrows=5)
        )

        reader = pyarrow.RecordBatchStreamReader(ipc_stream)
        dataframe = reader.read_pandas()
        assert dataframe.shape == (5, 13)

    # Takes roughly 10s on a decent laptop
    @pytest.mark.slow
    @pytest.mark.parametrize(
        'object_summaries',
        ['nulls_and_unicode.parquet'],
        indirect=True
    )
    def test_10mb_rough_size(self, files):
        # Just a benchmark not doing any assertions
        list(ParquetHandler(iter(list(files) * 100), close_s3_files=False).
             handle())

    def test_with_no_files(self):
        with pytest.raises(NoFilesInDataset):
            list(ParquetHandler(iter([])).handle())

    def test_os_error_is_caught(self, monkeypatch):
        logger_mock = MagicMock()

        with mock.patch.object(ParquetHandler, 'logger', logger_mock):
            with pytest.raises(ServiceException):
                list(ParquetHandler(iter(['tests/data'])).handle())
        assert logger_mock.warning.is_called()

    @pytest.mark.parametrize(
        'order_by_latest,expected',
        [
            # Ascending.
            (False, {'a': [1, 2, 3], 'b': [None, 2, 3], 'c': [None, None, 3]}),
            # Descending
            (True, {'a': [3, 2, 1], 'b': [3, 2, None], 'c': [3, None, None]}),
        ],
    )
    def test_additive_schemas(self, order_by_latest, expected):
        df1 = pandas.DataFrame({'a': [1]})

        def _parquet_file1():
            with tempfile.NamedTemporaryFile() as f:
                df1.to_parquet(f.name)
                return pq.ParquetFile(f.name)

        input1 = MagicMock()
        input1.to_parquet_file = _parquet_file1
        input1.backend_type = 'some-backend_type'
        input1.path = 's3://some-path.parquet'
        input1.metadata = {'size': 1}
        input1.size = 1

        df2 = pandas.DataFrame({'a': [2], 'b': [2]})

        def _parquet_file2():
            with tempfile.NamedTemporaryFile() as f:
                df2.to_parquet(f.name)
                return pq.ParquetFile(f.name)

        input2 = MagicMock()
        input2.to_parquet_file = _parquet_file2
        input2.backend_type = 'some-backend_type'
        input2.path = 's3://some-path.parquet'
        input2.metadata = {'size': 1}
        input2.size = 1

        df3 = pandas.DataFrame({'a': [3], 'b': [3], 'c': [3]})

        def _parquet_file3():
            with tempfile.NamedTemporaryFile() as f:
                df3.to_parquet(f.name)
                return pq.ParquetFile(f.name)

        input3 = MagicMock()
        input3.to_parquet_file = _parquet_file3
        input3.backend_type = 'some-backend_type'
        input3.path = 's3://some-path.parquet'
        input3.metadata = {'size': 1}
        input3.size = 1

        files = [input1, input2, input3]
        if order_by_latest:
            # Flip the test input into descending order
            files.reverse()

        stream = ParquetHandler(
            iter(files),
            order_by_latest=order_by_latest,
        ).\
            handle()

        ipc_stream = b''.join(stream)

        reader = pyarrow.RecordBatchStreamReader(ipc_stream)
        dataframe = reader.read_pandas()

        expected_df = pandas.DataFrame(expected)

        print('dataframe')
        print(dataframe)
        print('expected_df')
        print(expected_df)
        pandas.testing.assert_frame_equal(dataframe, expected_df)


class TestParquetHandlerStressfully:
    xfail = pytest.mark.xfail

    PARQUET_TEST_FILES = [
        pytest.param('nonnullable.impala.parquet', marks=xfail),
        pytest.param('datapage_v2.snappy.parquet', marks=xfail),
        pytest.param('nullable.impala.parquet', marks=xfail),

        # Working cases
        'nulls.snappy.parquet',
        'binary.parquet',
        'alltypes_plain.snappy.parquet',
        'fixed_length_decimal_legacy.parquet',
        'fixed_length_decimal.parquet',
        'nation.dict-malformed.parquet',
        'alltypes_dictionary.parquet',
        'dict-page-offset-zero.parquet',
        'int32_decimal.parquet',
        'byte_array_decimal.parquet',
        'int64_decimal.parquet',
        'single_nan.parquet',
        'alltypes_plain.parquet',
        'nested_maps.snappy.parquet',
        'nested_lists.snappy.parquet',
        'repeated_no_annotation.parquet',
        'nested2.snappy.parquet'
    ]

    @pytest.mark.parametrize(
        'object_summaries',
        ['empty.snappy.parquet'],
        indirect=True
    )
    def test_empty_parquet_files(self, files):
        ipc_stream = b''.join(
            ParquetHandler(iter(list(files))).handle()
        )

        reader = pyarrow.RecordBatchStreamReader(ipc_stream)
        df = reader.read_pandas()
        assert df.shape == (0, 2)

    @pytest.mark.parametrize(
        'object_summaries',
        PARQUET_TEST_FILES,
        indirect=True
    )
    def test_parquet_files(self, files):
        ipc_stream = b''.join(
            ParquetHandler(iter(list(files))).handle()
        )

        reader = pyarrow.RecordBatchStreamReader(ipc_stream)
        reader.read_pandas()

    @pytest.mark.parametrize(
        'object_summaries',
        PARQUET_TEST_FILES,
        indirect=True
    )
    def test_parquet_files_can_be_joined(self, files):

        try:
            ipc_stream = b''.join(
                ParquetHandler(iter(list(files) * 3), close_s3_files=False).
                    handle()
            )
        except ArrowNotImplementedError:
            pytest.fail('Unable to parse this type of parquet')

        reader = pyarrow.RecordBatchStreamReader(ipc_stream)
        reader.read_pandas()

    @pytest.mark.performance
    def test_generate_random_parquet_for_benchmark(self, benchmark):
        """Useful for generating a large randomised .parquet file"""
        # Rows:
        # 100 -> 205.5 kB (205,548 bytes) on disk in 0.44 seconds.
        # 10000 -> 9.2 MB (9,234,131 bytes) on disk in 0.67 seconds.

        nrows = 10000
        # Max columns should match a worst case. For CDS Single Name Pricing
        # Sensitivities and Liquidity there are 164 columns.
        max_columns = 168

        num_column_types = 6

        # Seed the random number generator so that we can reproduce the output.
        numpy.random.seed(0)

        def bools_df():
            return pandas.DataFrame(
                numpy.random.choice(
                    [False, True],
                    size=(nrows, int(max_columns / num_column_types))
                ),
                columns=[str(f'column_bool_{x}') for x in
                         range(int(max_columns / num_column_types))],
            )

        def ints_df():
            return pandas.DataFrame(
                numpy.random.randint(
                    low=0,
                    high=1000000,
                    size=(nrows, int(max_columns / num_column_types))
                ),
                columns=[str(f'column_int_{x}') for x in
                         range(int(max_columns / num_column_types))],
            )

        def floats_df():
            return pandas.DataFrame(
                numpy.random.rand(
                    nrows,
                    int(max_columns / num_column_types)),
                columns=[str(f'column_float_{x}') for x in
                         range(int(max_columns / num_column_types))],
            )

        def string_df():
            import pandas.util.testing
            return pandas.DataFrame(
                numpy.random.choice(
                    pandas.util.testing.RANDS_CHARS,
                    size=(nrows, int(max_columns / num_column_types))
                ),
                columns=[str(f'column_str_{x}') for x in
                         range(int(max_columns / num_column_types))],
            )

        def dates_df():
            dates = pandas.date_range(start='1970-01-01', end='2020-01-01')

            return pandas.DataFrame(
                numpy.random.choice(
                    dates,
                    size=(nrows, int(max_columns / num_column_types))
                ),
                columns=[str(f'column_date_{x}') for x in
                         range(int(max_columns / num_column_types))],
            )

        def datetimes_df():
            datetimes = pandas.date_range(start='1970-01-01', end='2020-01-01',
                                          freq='H')

            return pandas.DataFrame(
                numpy.random.choice(
                    datetimes,
                    size=(nrows, int(max_columns / num_column_types))
                ),
                columns=[str(f'column_datetime_{x}') for x in
                         range(int(max_columns / num_column_types))],
            )

        df = pandas.concat(
            [bools_df(), ints_df(), floats_df(), string_df(), dates_df(),
             datetimes_df()],
            # Concat columns axis
            axis=1,
            copy=False
        )

        # Randomise the column order so the compression cannot optimise
        # easily based on types as this will mix float columns among the int
        # columns.
        random_column_order = df.columns.tolist()
        random.shuffle(random_column_order)
        df = df[random_column_order]

        assert df.shape[0] == nrows
        assert df.shape[1] == max_columns

        filename = 'randomised_benchmark.parquet'

        def to_parquet():
            df.to_parquet(fname=filename)
            return None

        benchmark(to_parquet)
        # Check that we can read from the file that was written.
        pandas.testing.assert_frame_equal(pandas.read_parquet(filename), df)

    def test_raise_exception_for_invalid_first_parquet(
        self,
        monkeypatch,
        files
    ):
        """
        Assert that the stream from the handler still has a
        termination marker even if there's an exception
        """
        logger_mock = MagicMock()
        with mock.patch.object(ParquetHandler, 'logger', logger_mock):

            expected_df = pandas.DataFrame(
                data=[['aaa', 'bbb']], columns=['a', 'b'])

            def _not_parquet_file():
                with tempfile.NamedTemporaryFile() as f:
                    # Write a csv instead of a parquet.
                    expected_df.to_csv(f.name)
                    return pq.ParquetFile(f.name)

            input1 = MagicMock()
            input1.to_parquet_file = _not_parquet_file
            input1.backend_type = 'some-backend_type'
            input1.path = 's3://some-path.parquet'
            input1.metadata = {'size': 1}
            input1.size = 1

            with pytest.raises(ServiceException) as exc:
                ParquetHandler(iter([input1]))
            print(f"** pyarrow 2.0.0 exc.type: {exc.type}")
            assert exc.match(
                r'^Non parquet file found in dataset. Path: '
                r's3://some-path.parquet'
            )

    def test_raise_exception_for_invalid_not_first_parquet(
        self,
        monkeypatch,
        files
    ):
        """
        Assert that the stream from the handler still has a
        termination marker even if there's an exception
        """
        logger_mock = MagicMock()
        with mock.patch.object(ParquetHandler, 'logger', logger_mock):

            expected_df = pandas.DataFrame(
                data=[['aaa', 'bbb']], columns=['a', 'b'])

            def _parquet_file():
                with tempfile.NamedTemporaryFile() as f:
                    expected_df.to_parquet(f.name)
                    return pq.ParquetFile(f.name)

            input1 = MagicMock()
            input1.to_parquet_file = _parquet_file
            input1.backend_type = 'some-backend_type'
            input1.path = 's3://some-path.parquet'
            input1.metadata = {'size': 1}
            input1.size = 1

            def _not_parquet_file():
                with tempfile.NamedTemporaryFile() as f:
                    # Write a csv instead of a parquet.
                    expected_df.to_csv(f.name)
                    return pq.ParquetFile(f.name)

            input2 = MagicMock()
            input2.to_parquet_file = _not_parquet_file
            input2.backend_type = 'some-backend_type'
            input2.path = 's3://some-path.parquet'
            input2.metadata = {'size': 1}
            input2.size = 1

            stream = ParquetHandler(iter([
                input1, input2
            ])).handle()

            with pytest.raises(ServiceException) as exc:
                list(stream)
            assert logger_mock.warning.is_called()

    def test_raise_when_initial_file_is_csv_in_parquet_dataset(
        self,
    ):
        """
        Assert that the stream from the handler still has a
        termination marker even if there's an exception
        """
        def _parquet_file():
            raise ArrowException()

        input1 = MagicMock()
        input1.to_parquet_file = _parquet_file
        input1.backend_type = 'some-backend_type'
        input1.path = 's3://some-path.csv'
        input1.metadata = {'size': 1}
        input1.size = 1

        with pytest.raises(NonParquetFilesInDataset) as exc:
            ParquetHandler(iter([input1]))
        assert exc.match('Non parquet file found in dataset. '
                         'Path: s3://some-path.csv')

    def test_raise_when_subsequent_file_is_csv_in_parquet_dataset(
        self,
    ):
        """
        Assert that the stream from the handler still has a
        termination marker even if there's an exception
        """

        expected_df = pandas.DataFrame(
            data=[['aaa', 'bbb']], columns=['a', 'b'])

        def _parquet_file():
            with tempfile.NamedTemporaryFile() as f:
                expected_df.to_parquet(f.name)
                return pq.ParquetFile(f.name)

        input1 = MagicMock()
        input1.to_parquet_file = _parquet_file
        input1.backend_type = 'some-backend_type'
        input1.path = 's3://some-path.parquet'
        input1.metadata = {'size': 1}
        input1.size = 1

        def _csv_file():
            raise ArrowException()

        input2 = MagicMock()
        input2.to_parquet_file = _csv_file
        input2.backend_type = 'some-backend_type'
        input2.path = 's3://some-path.csv'
        input2.metadata = {'size': 1}
        input2.size = 1

        with pytest.raises(ServiceException) as exc:
            stream = ParquetHandler(iter([
                input1, input2
            ])).handle()
            list(stream)

    def test_skips_file_when_subsequent_file_is_zero_bytes(
        self,
    ):
        """
        Assert that the stream from the handler still has a
        termination marker even if there's an exception
        """

        expected_df = pandas.DataFrame(
            data=[['aaa', 'bbb']], columns=['a', 'b'])

        def _parquet_file():
            with tempfile.NamedTemporaryFile() as f:
                expected_df.to_parquet(f.name)
                return pq.ParquetFile(f.name)

        input1 = MagicMock()
        input1.to_parquet_file = _parquet_file
        input1.backend_type = 'some-backend_type'
        input1.path = 's3://some-path.parquet'
        input1.metadata = {'size': 1}
        input1.size = 1

        input2 = MagicMock()
        input2.to_parquet_file = _parquet_file
        input2.backend_type = 'some-backend_type'
        input2.path = 's3://some-path.csv'
        input2.metadata = {'size': 0}
        input2.size = 0

        stream = ParquetHandler(iter([
            input1, input2
        ])).handle()

        ipc_stream = b''.join(stream)

        reader = pyarrow.RecordBatchStreamReader(ipc_stream)
        df = reader.read_pandas()
        assert df.shape == (1, 2), 'Must only have the number of rows from ' \
                                   'one file (where the metadata is > 0 ' \
                                   'bytes), not rows from both files.'

    def test_skips_file_when_first_file_is_zero_bytes(
        self,
    ):
        expected_df = pandas.DataFrame(
            data=[['aaa', 'bbb']], columns=['a', 'b'])

        def _parquet_file():
            with tempfile.NamedTemporaryFile() as f:
                expected_df.to_parquet(f.name)
                return pq.ParquetFile(f.name)

        input1 = MagicMock()
        input1.to_parquet_file = _parquet_file
        input1.backend_type = 'some-backend_type'
        input1.path = 's3://some-path.parquet'
        input1.metadata = {'size': 0}
        input1.size = 0

        input2 = MagicMock()
        input2.to_parquet_file = _parquet_file
        input2.backend_type = 'some-backend_type'
        input2.path = 's3://some-path.parquet'
        input2.metadata = {'size': 1}
        input2.size = 1

        stream = ParquetHandler(iter([
            input1, input2
        ])).handle()

        ipc_stream = b''.join(stream)

        reader = pyarrow.RecordBatchStreamReader(ipc_stream)
        df = reader.read_pandas()

        assert ipc_stream[-8:] == IPC_STREAM_END
        assert df.shape == (1, 2), 'Must only have the number of rows from ' \
                                   'one file (where the metadata is > 0 ' \
                                   'bytes), not rows from both files.'


class TestParquetHandlerDictionaryTypes:
    def test_can_handle_basic_dictionary_types(self):
        array = pyarrow.DictionaryArray.from_arrays(
            pyarrow.array([0, 1, 3], type=pyarrow.int32()),
            pyarrow.array(['abc', 'def', 'gef', 'a', 'd'],
                          type=pyarrow.string())
        )

        schema = pyarrow.schema([
            pyarrow.field('a', array.type)
        ])

        batch = pyarrow.RecordBatch.from_arrays([array], schema=schema)

        table = pyarrow.Table.from_batches([batch, batch])

        expected_df = table.to_pandas()

        def _parquet_file():
            with tempfile.NamedTemporaryFile() as f:
                expected_df.to_parquet(f.name)
                return pq.ParquetFile(f.name)

        input1 = MagicMock()
        input1.to_parquet_file = _parquet_file
        input1.backend_type = 'some-backend_type'
        input1.path = 's3://some-path.parquet'
        input1.metadata = {'size': 1}
        input1.size = 1

        stream = ParquetHandler(iter([input1])).handle()

        ipc_stream = b''.join(stream)

        reader = pyarrow.RecordBatchStreamReader(ipc_stream)
        dataframe = reader.read_pandas()

        pandas.testing.assert_frame_equal(dataframe, table.to_pandas())

    def test_pandas_categorical(self):
        arrays = {
            'str': pandas.Series([
                str(x) for x in range(10000)]
            ).astype('category')
        }

        expected_df = pandas.DataFrame(arrays)

        def _parquet_file():
            with tempfile.NamedTemporaryFile() as f:
                expected_df.to_parquet(f.name)
                return pq.ParquetFile(f.name)

        input1 = MagicMock()
        input1.to_parquet_file = _parquet_file
        input1.backend_type = 'some-backend_type'
        input1.path = 's3://some-path.parquet'
        input1.metadata = {'size': 1}
        input1.size = 1

        stream = ParquetHandler(iter([input1])).handle()

        ipc_stream = b''.join(stream)

        reader = pyarrow.RecordBatchStreamReader(ipc_stream)
        dataframe = reader.read_pandas()

        pandas.testing.assert_frame_equal(dataframe, expected_df)
