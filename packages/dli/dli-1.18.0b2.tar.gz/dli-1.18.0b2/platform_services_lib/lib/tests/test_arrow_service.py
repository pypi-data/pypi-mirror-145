#
# Copyright (C) 2019 IHS Markit.
# All Rights Reserved
#

import pytest
from unittest.mock import MagicMock
import io
from pyarrow import RecordBatchStreamWriter, schema, field, RecordBatch

from .conftest import IPC_STREAM_END
from ..services.arrow_service import ArrowService
from ..services.exceptions import ServiceException
from ..services.arrow_service.exceptions import UnsupportedDatasetFormat
from ..services.arrow_service.handlers.stream_errors import (
    handle_arrow_stream_errors
)


@pytest.fixture
def file_service():
    service = MagicMock()
    yield service


@pytest.fixture
def arrow_service(dlc_service, file_service):
    yield ArrowService(file_service=file_service, dlc_service=dlc_service)


class TestArrowService:
    def test_use_correct_handler(self, dlc_service,
                                 file_service, arrow_service):
        handler = MagicMock()
        arrow_service.format_handlers['parquet'] = handler
        list(arrow_service.dataset_to_ipc_arrow_stream({
            'id': '123',
            'attributes': {
                'name': 'abc',
                'data_format': 'parquet'
            }
        }))
        assert handler().handle.called

    def test_exception_raised_if_no_handler(self, dlc_service,
                                            file_service, arrow_service):
        arrow_service.format_handlers = {}
        with pytest.raises(UnsupportedDatasetFormat):
            list(arrow_service.dataset_to_ipc_arrow_stream({
                'id': '123',
                'attributes': {
                    'name': 'abc',
                    'data_format': 'unknown'
                }
            }))

    def test_error_handler_closes_when_no_error(self):
        output = io.BytesIO()
        test_schema = schema([field('a', 'int64')])
        batch = RecordBatch.from_arrays([[1]], ['a'])

        with handle_arrow_stream_errors(
            RecordBatchStreamWriter(output, test_schema)
        ) as writer:
            writer.write_batch(batch)

        output.seek(0)
        output = output.read()
        assert output[-8:] == IPC_STREAM_END

    def test_error_handler_closes_when_if_error(self):
        output = io.BytesIO()
        test_schema = schema([field('a', 'int64')])
        # Invalid batch
        batch = RecordBatch.from_arrays([['abc']], ['b'])

        with pytest.raises(ServiceException) as exc:
            with handle_arrow_stream_errors(
                RecordBatchStreamWriter(output, test_schema)
            ) as writer:
                writer.write_batch(batch)

        output.seek(0)
        output = output.read()
        assert output[-8:] == IPC_STREAM_END
        # Assert exception bubbled up correctly
        assert exc.value.details == (
            "Unknown Exception in arrow stream. This could be a problem with "
            "the file you are trying to read. Please report the problem to "
            "the datalake platform team at DataLake-Support_L1@ihsmarkit.com. "
            "Please include the full error message including the request_id."
        )
