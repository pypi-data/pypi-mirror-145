import logging
from functools import partial
from typing import List, Dict, Iterator, Callable, Optional, Iterable
from boto3 import Session as Boto3Session

from ..view_exceptions import NotFound
from ...adapters.s3_io_adapters import ServiceIO
from ...handlers.s3_dataset_handler import S3DatasetHandler, S3PathDetails
from ..exceptions import UnableToAccessDataset, UnableToAuthenticateToS3

logger = logging.getLogger(__name__)


class ConsumptionDatasetHandler(S3DatasetHandler):

    '''
    This class implements the handle() method of the s3 dataset handler. We keep this separate, since it sits in lib.
    Consumption and S3Proxy use the same class, but diverge in how the handling of the paths is returned, for instance,
    one sorts and filters out hidden prefixes.
    '''


    # @ see FileService/CachedFetcherService

    def handle(self, dataset: Dict, query_partitions: Optional[Iterable]) -> Iterator[ServiceIO]:

        bucket_name = dataset['attributes']['location']['s3']['bucket']

        def _s3file_wrapper(dataset: dict, resource) -> Iterator[ServiceIO]:
            """
            Abstract over the S3 location and return a list of IO objects.

            :param: dataset - dictionary representing the dataset

            :return: List of S3 files.
            """
            prefix = dataset['attributes']['location']['s3']['prefix']
            prefix = prefix + ('' if prefix.endswith('/') else '/')

            # We want the most recent partition first so we get the most recent schema at the start of the S3 list.
            order_by_latest = True

            s: Callable[[Iterator[str]], Iterator[str]] = partial(  # type: ignore
                    S3DatasetHandler.filter_hidden_prefixes_by_dataset_content_and_load_type,
                    dataset['attributes'].get("content_type"),
                    dataset['attributes'].get("load_type"),
                    prefix,
                    order_by_latest,
                    query_partitions,
                )

            files_in_non_hidden_prefixes: Iterator[S3PathDetails] = self.get_s3_list_filter(
                resource,
                bucket_name=bucket_name,
                prefix=prefix,
                absolute_path=False,
                prefix_filter_fn=s,  # type: ignore
            )

            handles = S3DatasetHandler.convert_list_to_file_handles(resource, bucket_name, files_in_non_hidden_prefixes)
            yield from handles

        if 'location' in dataset['attributes']:
            location_s3: Dict = dataset['attributes']['location']['s3']
        else:
            raise UnableToAccessDataset(
                details=(
                    'You do not have access to this dataset. You must '
                    'request access to the dataset\'s package.'
                )
            )

        try:
            role_arn = location_s3.get('aws_role_arn')
            session: Boto3Session = self.create_session(role_arn=role_arn)
            resource = session.resource('s3')
        except UnableToAuthenticateToS3:
            logger.warning('Missing role_arn', extra={
                'dataset location s3': location_s3
            })
            raise

        try:
            for s3file in _s3file_wrapper(dataset, resource):
                yield s3file
        except resource.meta.client.exceptions.NoSuchBucket as e:
            raise NotFound(
                f'S3 bucket {bucket_name} does not exist'
            ) from e

    def list(self, accessible_datasets: List, organisation_shortcode: str, args, method_name: str):
        pass

    def __repr__(self):
        return "ConsumptionDatasetHandler"
