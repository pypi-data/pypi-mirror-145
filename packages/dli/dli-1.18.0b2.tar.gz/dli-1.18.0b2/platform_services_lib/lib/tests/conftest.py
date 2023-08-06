import os
from typing import Optional

from flask import Blueprint
from flask import Flask
from moto import mock_s3, mock_sts
from pymemcache import HashClient
from injector import singleton, Injector

from ..providers.memcache_provider import MemcachedDependencyProvider
from ..providers.oidc_provider import JWT, JWTEncoded
from ..authentication.middleware import ServiceMiddleware
from ..providers.ttlcache_provider import InMemoryTTLCacheDependencyProvider
from ..services.datadog_service.datadog_service import DataDogService

import hypothesis
import pytest
from unittest.mock import MagicMock
from pymemcache.test.utils import MockMemcacheClient


# --------------------------------------------------------------
# ARROW


IPC_STREAM_END = b'\xff\xff\xff\xff\x00\x00\x00\x00'

# --------------------------------------------------------------
# MIDDLEWARE

key = 'secret'
aud = 'some-audience'

def mock_middleware_server(views: Blueprint):

    def create_app():
        os.environ["CATALOGUE_API_URL"] = "test"
        application = Flask(__name__)
        application.wsgi_app = ServiceMiddleware(application.wsgi_app)
        application.injector = Injector()
        application.injector.binder.bind(DataDogService, MagicMock())

        # we need to access the injector in the wsgi (early), so we ascribe it to the object too
        application.register_blueprint(views)
        application.wsgi_app.injector = application.injector

        return application

    return create_app()


@pytest.fixture
def disconnected_middleware_client():

    views = Blueprint('middleware', __name__)
    HTTP_METHODS = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']

    @views.route(
        '/',
        methods=HTTP_METHODS
    )
    @views.route(
        '/<path:optional_path>',
        methods=HTTP_METHODS
    )
    def test_route(optional_path: Optional[str] = None):
        resp = MagicMock()
        resp.status_code = 200
        resp.headers = {}
        resp.content = "HELLO, WORLD"
        return resp.content, resp.status_code, resp.headers.items()

    @views.route(
        '/direct_test',
        methods=HTTP_METHODS
    )
    def test_direct_route(optional_path: Optional[str] = None):
        resp = MagicMock()
        resp.status_code = 403
        resp.headers = {}
        resp.content = "BE GONE, DRAGON"
        return resp.content, resp.status_code, resp.headers.items()

    os.environ['JWT_SECRET_KEY'] = key
    os.environ['JWT_AUDIENCE'] = aud
    app = mock_middleware_server(views)
    with app.test_client() as client:
        yield client


# --------------------------------------------------------------
# DL APP

@pytest.fixture
def platform_base_app_blueprint():
    """
    App with injector and no dependencies
    """
    app = Flask(__name__)

    class Dependencies:
        def __init__(
                self,
        ):

            self.memcached = MemcachedDependencyProvider(
                elasticache_config_node_url=os.environ.get(
                    'ELASTICACHE_CONFIG_NODE_URL'
                ),
                default_ttl=int(os.environ.get(
                    'DEFAULT_CACHE_TTL', 3600
                ))
            )

            self.ttl_cache = InMemoryTTLCacheDependencyProvider()

    app.dependencies = Dependencies()

    app.injector = Injector([
        app.dependencies.memcached,
        app.dependencies.ttl_cache
    ])

    with app.app_context():
        yield app


@pytest.fixture
def jwt():
    """
    Raw jwt
    """
    yield


@pytest.fixture
def user():
    """
    Stub user. Will just pass with no auth.
    """
    yield


@pytest.fixture
def platform_app_blueprint(platform_base_app_blueprint, user, jwt):
    """
    App with authentication disabled.

    All datalake platform python apps have an .injector,
    and a .dependencies "Dependencies" class (one which has named attributes)

    Those named attributes refer to a provider of a typed annotated argument
    e.g. MemcachedDependencyProvider ultimately provides type: HashClient
    """

    dependencies = [
        (JWT, user, singleton),
        (JWTEncoded, jwt, singleton),
        (HashClient, MockMemcacheClient(), singleton),
    ]

    for key, mock, scope in dependencies:
        platform_base_app_blueprint.injector.binder.bind(key, mock, scope)

    yield platform_base_app_blueprint


@pytest.fixture
def platform_app_client(platform_app_blueprint):
    platform_app_blueprint.testing = True
    yield platform_app_blueprint.test_client()


# ---------------------------------------------------------------
# SERVICE MOCKS

@pytest.fixture
def aws_s3():
    """Set up Mock S3"""
    with mock_s3() as s3:
        yield s3


@pytest.fixture
def aws_sts():
    """Set up Mock S3"""
    with mock_sts() as sts:
        yield sts


@pytest.fixture
def dlc_service():
    service = MagicMock()
    yield service


# ---------------------------------------------------------------
# HYPOTHESIS

hypothesis.settings.register_profile(
    'ci',
    deadline=1000,
    suppress_health_check=[hypothesis.HealthCheck.too_slow],
)
hypothesis.settings.load_profile(os.getenv(u'HYPOTHESIS_PROFILE', 'default'))
