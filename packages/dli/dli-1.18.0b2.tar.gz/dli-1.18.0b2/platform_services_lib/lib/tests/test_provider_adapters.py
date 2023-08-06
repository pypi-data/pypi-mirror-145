#
# Copyright (C) 2019 IHS Markit.
# All Rights Reserved
#

import pytest
from injector import singleton
from urllib3.response import HTTPResponse
from unittest.mock import MagicMock

from ..providers.catalogue_provider import (
    JWTDependencyProvider
)
from ..providers.identity_provider import JWTIdentityDependencyProvider
from ..providers.oidc_provider import JWTEncoded


class TestProviderAdapters:

    @pytest.fixture(autouse=True)
    def jwt(self):
        """Overrides empty JWT header"""
        yield 'abc'

    @pytest.fixture
    def platform_app_blueprint(self, platform_base_app_blueprint, jwt):
        # this should override `platform_app_blueprint` of conftest

        # we install our matcher to the base app blueprint
        platform_base_app_blueprint.injector.binder.bind(
            JWTEncoded, jwt, singleton
        )

        yield platform_base_app_blueprint

    def test_jwt_is_sent_on_catalogue_adapter(self, platform_app_blueprint, monkeypatch):

        response = MagicMock()
        urlopen = response().connection_from_url().urlopen
        urlopen.return_value = HTTPResponse()
        monkeypatch.setattr(
            'requests.adapters.PoolManager', response
        )

        provider = JWTDependencyProvider(api_root='http://localhost/')
        session = provider.auth_client()
        session.get('http://localhost/')
        request = urlopen.call_args[1]

        assert request['headers']['Authorization'] == 'Bearer abc'
        assert request['headers']['User-Agent'] == 'consumption / unknown'

    def test_jwt_is_send_on_identity_adapter(self, platform_app_blueprint, monkeypatch):
        response = MagicMock()
        urlopen = response().connection_from_url().urlopen
        urlopen.return_value = HTTPResponse()
        monkeypatch.setattr(
            'requests.adapters.PoolManager', response
        )

        provider = JWTIdentityDependencyProvider(api_root='http://localhost/')
        session = provider.auth_client()
        session.get('http://localhost/')
        request = urlopen.call_args[1]

        assert request['headers']['Authorization'] == 'Bearer abc'
        assert request['headers']['User-Agent'] == 'consumption / unknown'
