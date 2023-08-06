#
# Copyright (C) 2019 IHS Markit.
# All Rights Reserved
#
import boto3
import jwt
import pytest

from botocore.awsrequest import AWSRequest
from datetime import datetime, timedelta
from flask import current_app, jsonify
from flask_injector import FlaskInjector

from ..services.view_exceptions import UnprocessableEntity, BaseHttpException
from ..providers.oidc_provider import JWT, OIDCDependencyProvider

AUD = KEY = 'test'


class TestOIDCAuthentication:

    @pytest.fixture
    def platform_app_blueprint(self, platform_base_app_blueprint):
        # this should override `platform_app_blueprint` of conftest

        # we install our matcher to the base app blueprint
        platform_base_app_blueprint.injector.binder.install(
            OIDCDependencyProvider(key=KEY, audience=AUD, verify_aud=True, verify_exp=True, verify_signature=True)
        )

        yield platform_base_app_blueprint

    @pytest.fixture(autouse=True)
    def error_to_status_code_view(self, platform_app_blueprint):

        # most dl-app's use some form of bubble up for exceptions (esp. BaseHttpException / HTTPException).
        # the bubbled up exception is then turned into a status_code, json blob of the exception
        # e.g. raise Unauthorized () -> wsgi 401, {message: Unauthorized}

        @platform_app_blueprint.errorhandler(BaseHttpException)
        def handle_exception(exception):
            """
            Handle exceptions raised by our app
            """
            exception_json = exception.to_dict()
            response = jsonify(exception_json)
            response.status_code = exception.status_code
            return response

    @pytest.fixture(autouse=True)
    def jwt_test_view(self, platform_app_blueprint):
        # we add a test view
        def _test_func():
            try:
                jwt = current_app.injector.get(JWT)
                return jsonify(jwt)
            except Exception as e:
                print(f'Test endpoint raising error with status code {e.status_code}, description {e.description}')
                raise

        platform_app_blueprint.add_url_rule('/test/', 'test', _test_func)

        # IMPORTANT!! One MUST set up Flask injector AFTER views have been added.
        # If you do not, you will be in a world of pain trying to understand why Injector methods are not entered
        # and why Request (arg of providers) doesnt have positional arg "environ"

        FlaskInjector(app=platform_app_blueprint, injector=platform_app_blueprint.injector)
        yield platform_app_blueprint

    @pytest.fixture
    def decoded_jwt(self):
        return {
            'sub': "1234567890",
            'name': "John Doe",
            'aud': AUD,
            'iat': 1516239022,
            'exp': (datetime.now() + timedelta(hours=1)).timestamp()
        }

    def test_accept_valid_jwt_from_cookie(self, platform_app_client, decoded_jwt):
        token = self._encode_token(decoded_jwt, KEY)
        platform_app_client.set_cookie('localhost', 'oidc_id_token', token)

        response = platform_app_client.get('/test/')
        assert response.json == decoded_jwt

    def test_rejects_jwt_bad_key_from_cookie(self, platform_app_client, decoded_jwt):
        token = jwt.encode(
            decoded_jwt, 'incorrect_secret',
        )
        platform_app_client.set_cookie('localhost', 'oidc_id_token', token)

        response = platform_app_client.get('/test/')

        assert response.status_code == 401
        assert response.json['description'] == ('User not authenticated. '
                                                'Invalid Signature: Signature '
                                                'verification failed.')

    def test_rejects_nonsense_from_cookie(self, platform_app_client):
        platform_app_client.set_cookie('localhost', 'oidc_id_token', 'blah blah blah')
        response = platform_app_client.get('/test/')
        assert response.status_code == 401
        assert response.json['description'] == ('User not authenticated. '
                                                'Invalid Token: Not enough '
                                                'segments.')

    def test_rejects_expired_token_from_cookie(self, platform_app_client, decoded_jwt):
        decoded_jwt['exp'] = (datetime.now() - timedelta(hours=1)).timestamp()
        token = self._encode_token(decoded_jwt, KEY)
        platform_app_client.set_cookie('localhost', 'oidc_id_token', token)

        response = platform_app_client.get('/test/', )

        assert response.status_code == 401
        assert response.json['description'] == ('User not authenticated. '
                                                'Expired Signature: Signature '
                                                'has expired.')

    def test_accept_valid_auth_header(self, platform_app_client, decoded_jwt):
        token = self._encode_token(decoded_jwt, KEY)
        auth_header = {'Authorization': 'Bearer ' + token}

        response = platform_app_client.get('/test/', headers=auth_header)

        assert response.json == decoded_jwt

    def test_rejects_auth_header_without_bearer_prefix(self, platform_app_client, decoded_jwt):
        token = self._encode_token(decoded_jwt, KEY)
        auth_header = {'Authorization': token}

        response = platform_app_client.get('/test/', headers=auth_header)

        assert response.status_code == 422
        assert response.json['description'] == (
            'User cannot be authenticated. '
            'Authorization Header type not '
            'provided.'
        )

    def test_rejects_jwt_bad_key_from_auth_header(self, platform_app_client,
                                                  decoded_jwt):

        token = self._encode_token(decoded_jwt, 'incorrect_secret')
        auth_header = {'Authorization': 'Bearer ' + token}

        response = platform_app_client.get('/test/', headers=auth_header)

        assert response.status_code == 401
        assert response.json['description'] == ('User not authenticated. '
                                                'Invalid Signature: Signature '
                                                'verification failed.')

    def test_rejects_nonsense_from_auth_header(self, platform_app_client):
        auth_header = {'Authorization': 'Bearer whatever'}

        response = platform_app_client.get('/test/', headers=auth_header)

        assert response.status_code == 401
        assert response.json['description'] == ('User not authenticated. '
                                                'Invalid Token: Not enough '
                                                'segments.')

    def test_rejects_expired_token_from_auth_header(self, platform_app_client,
                                                    decoded_jwt):
        decoded_jwt['exp'] = (datetime.now() - timedelta(hours=1)).timestamp()
        token = self._encode_token(decoded_jwt, KEY)
        auth_header = {'Authorization': 'Bearer ' + token}

        response = platform_app_client.get('/test/', headers=auth_header)

        assert response.status_code == 401
        assert response.json['description'] == ('User not authenticated. '
                                                'Expired Signature: Signature '
                                                'has expired.')

    def test_rejects_request_with_cookie_and_header(self, platform_app_client, decoded_jwt):
        token = self._encode_token(decoded_jwt, KEY)
        platform_app_client.set_cookie('localhost', 'oidc_id_token', token)
        auth_header = {'Authorization': 'Bearer ' + token}

        response = platform_app_client.get('/test/', headers=auth_header)

        assert response.status_code == 422
        assert response.json['description'] == (
            'User cannot be authenticated. '
            'Only one token should be '
            'provided either in the '
            'Authorization Header or in '
            'the Cookie.'
        )

    def test_rejects_request_without_cookie_or_header(self, platform_app_client, decoded_jwt):
        response = platform_app_client.get('/test/')

        assert response.status_code == 401
        assert response.json['description'] == (
            'User not authenticated. Token has to be provided either in the Authorization Header .'
        )

    @staticmethod
    def _encode_token(decoded_jwt, secret):
        return jwt.encode(
            decoded_jwt, secret
        )


class TestBotoJWT:
    @pytest.fixture
    def jwt(self):
        return 'ACCESS_KEY'

    @pytest.fixture
    def awsrequest(self):
        return AWSRequest(
            url='/',
            method='GET',
            headers={},
        )

    @pytest.fixture
    def s3_client(self, jwt):
        return boto3.client(
            's3',
            aws_access_key_id=jwt,
            aws_secret_access_key='noop',
        )

    def test_valid_aws_boto_request(self, awsrequest, s3_client, jwt):
        s3_client._request_signer.sign('s3', awsrequest)

        extracted_jwt = OIDCDependencyProvider._get_aws_jwt(
            awsrequest.headers['Authorization']
        )
        assert extracted_jwt == jwt

    def test_valid_aws_spark_request(self, awsrequest, s3_client, jwt):
        extracted_jwt = OIDCDependencyProvider._get_aws_jwt(
            'AWS abc:xyz'
        )
        assert extracted_jwt == 'abc'

    def test_invalid_aws_request_raises(self):
        with pytest.raises(UnprocessableEntity):
            OIDCDependencyProvider._get_aws_jwt(
                'abc'
            )
