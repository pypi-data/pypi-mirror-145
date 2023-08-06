import logging
import os
import uuid
from enum import Enum

import jwt
import requests
from urllib.parse import urljoin
from typing import Optional

from ..context.environments import _Environment
from ..context.urls import identity_urls
from ..providers.oidc_provider import JWTEncoded
from ..services.view_exceptions import Unauthorized
from ..context.dev_mode_testing import _get_token

logger = logging.getLogger(__name__)


class ClientCredentialsAuthenticationMethod(str, Enum):
    pat = 'pat'
    application = 'application'

    def __str__(self):
        return self.value


def _sam_app_flow(environment: _Environment, user_id: str, user_secret: str, origin=None) -> str:
    """Exchange the Application user's credentials provided by the user for a Catalogue token in the form of a JWT"""

    logger.info("Exchanging application user credentials")

    return __token_exchange(
        environment=environment,
        user_id=user_id,
        user_secret=user_secret,
        authentication_method=ClientCredentialsAuthenticationMethod.application,
    )


def external_session():
    return requests.Session()


def _sam_pat_flow(environment: _Environment, user_id: str, user_secret: str) -> str:
    """Exchange the PAT user's credentials provided by the user for a Catalogue token in the form of a JWT"""

    logger.info("Exchanging PAT user credentials")

    return __token_exchange(
        environment=environment,
        user_id=user_id,
        user_secret=user_secret,
        authentication_method=ClientCredentialsAuthenticationMethod.pat,
    )


def __token_exchange(
    environment: _Environment,
    user_id: str,
    user_secret: str,
    authentication_method: ClientCredentialsAuthenticationMethod,
) -> str:
    """Exchange the credentials provided by the user for a Catalogue token in the form of a JWT"""

    logger.info("Exchanging credentials for a Catalogue token", extra={'authentication_method': authentication_method})

    if user_id is None:
        logger.warning("User ID is not set")

    if user_secret is None:
        logger.warning("User Secret is not set")

    if environment.catalogue is None:
        logger.warning("Catalogue Endpoint is not set")

    token_exchange_url = urljoin(environment.catalogue, identity_urls.identity_token_exchange)  # type: ignore

    dl_payload = {
        'username': user_id,
        'password': user_secret,
        'auth_method': authentication_method.value,  # Must send the string value not the enum.
    }

    if os.environ.get('DEV_MODE'):
        # Dev test mode, returns a test jwt that will authenticate against test containers.
        # This represents the token exchange. This allows for writing integration tests with App and PAT users.
        # TODO We would like to change this block to be an interface on auth.py to remove this from production code
        return _get_token(os.environ.get('JWT_SECRET_KEY', 'secret'))

    else:
        resp = external_session().post(token_exchange_url, json=dl_payload)
        if resp.status_code != 200:
            message = f'Could not exchange user credentials for JWT access token via the Catalogue with auth_method=:{authentication_method.value}'
            logger.warning(
                message,
                extra={
                    'response_status_code': resp.status_code,
                    'response_content': resp.text,
                    'authentication_method': authentication_method.value,
                }
            )
            raise Unauthorized(message)

        response_jwt = resp.json()['access_token']
        return response_jwt


def decode_token(key):

    __pyjwt_algorithms = [
        # `HS256` is the value returned by the JWT from prod, but pyjwt seems
        # to complain about the signature.
        'HS256',
        'HS512', 'ES256', 'ES384', 'ES512', 'RS256', 'RS384',
        'RS512', 'PS256', 'PS384', 'PS512',
    ]

    return jwt.decode(
        jwt=key,
        algorithms=__pyjwt_algorithms,
        options={
            "verify_signature": False,
            "verify_aud": False,
            "verify_exp": False
        }
    )


def _pre_request_get_token(environment: _Environment, user_id: str, user_secret: str, hint: Optional[str]) -> JWTEncoded:

    _PAT = "PAT"
    _JWT = "JWT"
    _APP = "APP"

    if user_id is None or user_secret is None:
        raise Unauthorized()

    if not hint or hint == _PAT:
        # we think its a PAT or want to check it matches a UUID (which indicates it is)
        try:
            # is this a uuid as only PATs are UUIDs? - if it is it can be parse to UUID type
            uuid.UUID(user_id)
            return JWTEncoded(_sam_pat_flow(environment, user_id, user_secret))
        except (ValueError, TypeError) as e:
            logging.debug(f"{e} - doesn't look like a PAT {user_id}", exc_info=e)
            if hint == _PAT:
                raise e

    if not hint or hint == _JWT:
        # we think its already a JWT or want to check its valid
        try:
            # is this a JWT? - if it is it can be decoded
            decode_token(user_id)
            return JWTEncoded(user_id)  # the JWT
        except jwt.DecodeError as e:
            logging.debug(f"{e} - doesn't look like a JWT {user_id}", exc_info=e)
            if hint == _JWT:
                raise e

    if not hint or hint == _APP:
        # this seems to be an APP user, since its not a UUID or JWT
        try:
            return JWTEncoded(_sam_app_flow(environment, user_id, user_secret))
        except Exception as e:
            logging.debug(f"{e} - doesn't look like an APP {user_id}", exc_info=e)
            if hint == _APP:
                raise e

    raise Unauthorized()
