import base64
import logging
import os
import sys
import uuid
from typing import Optional, NewType, Tuple, Dict, Any, Mapping, List, Iterable

import jwt.exceptions
from flask import request
from requests.models import CaseInsensitiveDict, Response, Request

from ..authentication.auth import _pre_request_get_token, Unauthorized
from ..context.environments import _Environment
from ..providers.oidc_provider import JWTEncoded, OIDCDependencyProvider
from ..services.datadog_service.datadog_service import DataDogService
from ..services.exceptions import InterfaceResourceUnavailable

root = logging.getLogger()
root.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
from pythonjsonlogger import jsonlogger
formatter = jsonlogger.JsonFormatter('%(name)s %(process)d %(threadName)s %(asctime)s %(module)s %(lineno)d %(funcName)s %(levelname)s %(message)s %(pathname)s')
handler.setFormatter(formatter)
root.addHandler(handler)

########################################################################################################################
# The middleware relies on the application to inject a header in order to stay generic.
#
# Examples of how to bind the functions are shown in the 'Identity' (I) functions below, which do nothing.
# Albeit, any field of the original headers could be modified with the extracted JWT before sending to upstream.

# use to set injection of header modifier function
# defined by the type :: str, Dict -> Dict
HEADER_MODIFIER = NewType('HEADER_MODIFIER', str)
RESPONSE_MODIFIER = NewType('RESPONSE_MODIFIER', str)  # type: ignore
UNAUTHORIZED_MODIFIER = NewType('UNAUTHORIZED_MODIFIER', str)
EXCEPTION_MODIFIER = NewType('EXCEPTION_MODIFIER', str)


def identity_header_function(jwt: Optional[str], headers: Dict) -> Dict:
    # Add this to your flask app to bind this function, or provide your own
    #
    #     app.injector.binder.bind(
    #         HEADER_MODIFIER,
    #         to=lambda: identity_header_function,
    #         scope=request,
    #     )

    return headers


def identity_response_function(resp: Response) -> Tuple[Any, int, CaseInsensitiveDict]:
    # Add this to your flask app to bind this function, or provide your own
    #
    #     app.injector.binder.bind(
    #         RESPONSE_MODIFIER,
    #         to=lambda: identity_response_function,
    #         scope=request,
    #     )

    return resp.raw, resp.status_code, resp.headers


def identity_unauthorized_function(strt, code: str, headers: List[Tuple[str, str]], reason: str):
    # Add this to your flask app to bind this function, or provide your own
    #
    #     app.injector.binder.bind(
    #         UNAUTHORIZED_MODIFIER,
    #         to=lambda: identity_unauthorized_function,
    #         scope=request,
    #     )
    strt(code, headers)
    return reason


def identity_exception_function(strt, code: str, headers: List[Tuple[str, str]], e: Exception):
    # Add this to your flask app to bind this function, or provide your own
    #
    #     app.injector.binder.bind(
    #         EXCEPTION_MODIFIER,
    #         to=lambda: identity_exception_function,
    #         scope=request,
    #     )
    strt(code, headers)
    return str(e)


########################################################################################################################
# A flask middleware to be applied to the flask app - this resolves any possible latency or memory requirement
# caused by running as a separate server on the same pod
#
# This should be used as follows on creation of the flask app as follows:
#
#     app = Flask(__name__)
#     app.register_blueprint([views,...])
#
#     app.injector = Injector()
#     app.wsgi_app = ModifyHeaderMiddleware(app.wsgi_app)
#     app.wsgi_app.injector = app.injector
#

class AppIter(Iterable):
    def __init__(self, app_iter, datadog_service, app_name, oidc, jwt_encoded: JWTEncoded, path, method):
        self.app_iter = app_iter
        self.datadog_service = datadog_service
        self.app_name = app_name
        self.point_queue = []
        self.path = path
        self.method = method

        jwt_decoded: Dict = {}
        try:
            jwt_decoded: Dict = oidc.user_info(jwt_encoded)
        except Unauthorized as e:
            # Maybe the JWT has been tampered with.
            logging.warning('AppIter saw an Unauthorized JWT signature for send_metrics', exc_info=e)

        if jwt_decoded.get("system_user") and jwt_decoded.get("sub"):
            # App flow case
            self.uname = jwt_decoded["sub"]
            self.email = '-'

        elif jwt_decoded.get("name") and jwt_decoded.get("email"):
            # JWT + PAT flow case
            self.uname = jwt_decoded["name"]
            self.email = jwt_decoded["email"]

        else:
            # We cannot be sure who the user is so we should not attribute the username and email address.
            self.uname = '-'
            self.email = '-'

        if 'datalake' in jwt_decoded and 'organisation_id' in jwt_decoded["datalake"]:
            try:
                organisation = self.datadog_service.cached_fetcher_service.dlc_me(jwt=jwt_encoded)

                if 'data' in organisation and \
                        'attributes' in organisation['data'] and \
                        'name' in organisation['data']['attributes']:
                    self.organisation_name = organisation['data']['attributes']['name']
                else:
                    self.organisation_name = '-'

            except InterfaceResourceUnavailable as e:
                # jwt is invalid or expired
                self.organisation_name = f'expired: {jwt_decoded["datalake"]["organisation_id"]}'
                logging.warning('jwt is invalid or expired', exc_info=e)
        else:
            self.organisation_name = '-'

    def __iter__(self):
        return self

    def __next__(self, *args, **kwargs):
        def send_metrics():
            content_size = sum(self.point_queue)
            self.datadog_service.send_metric(
                'ihs.metrics.bytes',
                content_size, self.uname, self.email, self.organisation_name, self.path, self.method)
            self.point_queue = []

        try:
            chunk = next(self.app_iter)
            self.point_queue.append(len(chunk))
            if len(self.point_queue) >= int(os.environ.get('DD_SEND_METRICS_PER_POST', 1000)):
                send_metrics()
            return chunk

        except StopIteration as e:
            # This is not a tru exception, it is the way Python ends iteration.
            send_metrics()
            raise e


class ServiceMiddleware(object):

    MSG_NOT_AUTHORIZED = "User not authenticated"
    MSG_INTERNAL_NO_AUTH_HEADER = "No authorization header provided"
    MSG_INTERNAL_FAILED_AUTHENTICATE = "Failed authentication"
    MSG_TYPE_WARNING = "WARNING"
    MSG_TYPE_EXCEPTION = "EXCEPTION"
    MB = 1048576

    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app
        self.env = _Environment(os.environ["CATALOGUE_API_URL"])
        self.__oidc = OIDCDependencyProvider(
            key=os.environ.get('JWT_SECRET_KEY'),
            audience=os.environ.get('JWT_AUDIENCE'),
            # QA want to maintain the old behaviour of not allowing analytics for invalid JWT so that a user cannot
            # tamper with the JWT and attribute work to another user.
            verify_signature=True,
            verify_aud=False,
            verify_exp=False,
        )

    @staticmethod
    def unauthorized(msg, msg_type, start_response):
        if msg_type == ServiceMiddleware.MSG_TYPE_WARNING:
            root.warning(msg)
        else:
            root.exception(msg)

        start_response('401 Unauthorized', [('Content-Type', 'text/html')])
        return [ServiceMiddleware.MSG_NOT_AUTHORIZED.encode()]

    @staticmethod
    def exception(msg, e, start_response):
        root.exception(msg)

        start_response('500 Error', [('Content-Type', 'text/html')])
        return [str(e).encode()]

    @staticmethod
    def try_unauthorized(unauthorized_modifier_fn, start_response, reason):
        try:
            return unauthorized_modifier_fn(start_response, "401 Unauthorized",
                                            [('Content-Type', 'text/html')], reason)
        except Exception:
            return ServiceMiddleware.unauthorized(
                'Middleware `unauthorized` modifier exception', ServiceMiddleware.MSG_TYPE_EXCEPTION, start_response)

    @staticmethod
    def try_exception(exception_modifier_fn, start_response, e):
        try:
            return exception_modifier_fn(start_response, "500 Error",
                                         [('Content-Type', 'text/html')], str(e))
        except Exception as e:
            return ServiceMiddleware.exception('Middleware `exception` modifier exception', e, start_response)

    @staticmethod
    def extract_jwt_from_cookie(environ: Dict) -> Optional[str]:
        """
        Catalogue live preview does use cookies

        :param environ: request variables as a dict.
        """
        if environ.get("HTTP_COOKIE"):
            cookies_from_env: str = environ['HTTP_COOKIE']
            cookies: List[str] = cookies_from_env.split(";")
            cookie_filter_only_splittable: List[str] = [x for x in cookies if '=' in x]
            key_values: List[List[str]] = [x.split("=", 1) for x in cookie_filter_only_splittable]
            cookie_authorizer = "oidc_id_token"

            for k, v in key_values:
                # Strip whitespace from the key. We've seen a strange case on the dev env where the Catalogue adds
                # whitespace characters after the ";" in the cookie so our keys get prefixed with whitespace e.g.
                # " session"
                if k and v and cookie_authorizer == k.strip():
                    return v

    def __call__(self, environ: Dict, start_response):
        # before request to route, add some variables to the environ according to the app

        unauthorized_modifier_fn = self.injector.get(UNAUTHORIZED_MODIFIER)  # type: ignore
        exception_modifier_fn = self.injector.get(EXCEPTION_MODIFIER)  # type: ignore

        via_cookie_jwt = ServiceMiddleware.extract_jwt_from_cookie(environ)

        if not environ.get("HTTP_AUTHORIZATION") and not via_cookie_jwt:
            if unauthorized_modifier_fn:
                return self.try_unauthorized(unauthorized_modifier_fn, start_response, ServiceMiddleware.MSG_INTERNAL_NO_AUTH_HEADER)
            else:
                return ServiceMiddleware.unauthorized(
                    ServiceMiddleware.MSG_INTERNAL_NO_AUTH_HEADER, ServiceMiddleware.MSG_TYPE_WARNING, start_response)

        try:
            jwt_encoded: JWTEncoded = ServiceMiddleware._resolve(self.env, "HTTP_AUTHORIZATION", environ, via_cookie_jwt=via_cookie_jwt)
        except Exception as e:
            if unauthorized_modifier_fn:
                return self.try_unauthorized(unauthorized_modifier_fn, start_response, str(e))
            else:
                return ServiceMiddleware.unauthorized(
                    ServiceMiddleware.MSG_INTERNAL_FAILED_AUTHENTICATE, ServiceMiddleware.MSG_TYPE_WARNING, start_response)

        try:
            # everything must be in the try, since the app supplied modifier functions could blow up

            if not environ.get('HTTP_X_REQUEST_ID'):
                environ['HTTP_X_REQUEST_ID'] = str(uuid.uuid1())

            # this will likely set HTTP_AUTHORIZATION and any other headers it wants (prepended HTTP_)
            header_modifier_fn = self.injector.get(HEADER_MODIFIER)  # type: ignore

            if header_modifier_fn:
                # this will interfere with the request
                environ.pop('HTTP_HOST', None)

                # lets remove this to make clear that we later set it
                environ.pop('HTTP_AUTHORIZATION', None)

                # application itself is requesting a header modification be run before sending to its routes
                environ = header_modifier_fn(jwt_encoded, environ)

            response_status: int = 0
            response_headers: Mapping = {}

            def custom_start_response(status, environ={}):
                nonlocal response_status
                nonlocal response_headers
                response_headers = environ
                response_status = status
                # after response from route, intercept the response (applicable only on plain out)
                # route_response = start_response(status, environ)
                # return route_response

            # go to the route with pre-adjusted environ, and response callback
            # There is no point putting this in an exception, since even a 500 from the wsgi container
            # will return to here, sans exception e.g. 500 INTERNAL ERROR
            app_iter = self.wsgi_app(environ, custom_start_response)

            response_modifier = self.injector.get(RESPONSE_MODIFIER)  # type: ignore

            response_headers_dict: Dict = dict(response_headers)

            # DataDog expects integer type in the log's JSON.
            # TODO this is going to go to /me endpoint with a call, which delays return of call to user
            # TODO we could switch Datadogservice to use CachedFetcherService
            # TODO we could async/await on organisation_name (but we're using gevent anyway)
            app_iter = AppIter(
                app_iter,
                self.injector.get(DataDogService),  # type: ignore
                os.environ.get('DD_APPLICATION_NAME'),
                self.__oidc,
                jwt_encoded,
                path=environ.get('RAW_URI'),
                method=environ.get('REQUEST_METHOD')
            )

            if response_modifier and response_headers_dict.get('content-type') != 'binary/octet-stream':
                # recover the response as we still want to do some adjustment
                response_content_reread = b"".join(app_iter)
                dummy_response = Response()
                dummy_request = Request()
                dummy_response._content = response_content_reread
                dummy_request.headers = environ
                dummy_response.request = dummy_request  # type: ignore
                dummy_response.headers.update(response_headers)
                dummy_response.status_code = response_status

                # application itself is requesting a header modification be run before sending to its routes
                content, content_status, content_headers = response_modifier(dummy_response)
                start_response(str(content_status), list(dict(content_headers).items()))

                return [content]
            else:
                # if not modification needed, don't re-read, just return it* (this is an future)
                # based on the fact that you may still be writing/streaming the response in chunk
                # see https://stackoverflow.com/questions/16774952/wsgi-whats-the-purpose-of-start-response-function
                start_response(response_status, response_headers)
                return app_iter
        except Exception as e:
            root.exception('Middleware __call__ exception')
            if exception_modifier_fn:
                return self.try_exception(exception_modifier_fn, start_response, e)
            else:
                return ServiceMiddleware.exception(str(e), e, start_response)

    @staticmethod
    def _resolve(env, auth_header="Authorization", use_environ=None, via_cookie_jwt=None) -> JWTEncoded:
        # Authorization schemes seen in the Authorization HTTP header
        bearer_prefix = "Bearer"
        ldap_basic_prefix = "Basic"
        aws_v4_signed_prefix = "AWS4-HMAC-SHA256"
        aws_s3_rest_prefix = "AWS"

        # Delimiter character which divides username and password in single field scenarios
        # Non-presence of the delimiter indicates that it can only be a JWT flow
        auth_credential_delimiter = "\\"

        user = None       # extracted username or JWT (if extracted)
        password = None   # extract password or "NOP" (if extracted)
        hint = None       # type of credential        (if can be inferred)

        if use_environ is None and request.authorization is not None:
            # for BI tools - username/password style forms
            # we know for a fact its a Credential: (App user/pass) or (PAT user/pass) or (JWT/nop), but not which
            if not use_environ:
                user = request.authorization.username
                password = request.authorization.password
            else:
                # shouldn't be receiving a middleware request with wsgi environ, this will raise Unauthorized later
                pass

        elif via_cookie_jwt:
            # life-support for Consumption API Docs
            user, password, hint = (via_cookie_jwt, "NOP", "JWT")

        elif use_environ is not None or request.headers[auth_header] is not None:
            # we know this is either:
            # AMS4-HMAC-SHA256 <JWT>/... <User>:<Password>/.../.../  (v4 signing, used by AWS SDK [Spark/Boto etc])
            # AWS <JWT>/... <User>:<Password>/.../...                (s3 rest, used by AWS S3 over REST to spec. [CURL])
            # Bearer <JWT>                                           (Bearer, used by Datalake [S3-Proxy, Catalogue])
            # Basic <User>:<Password>                                (LDAP/Basic, [Presto])
            #
            # but we're not yet sure which, nor which Credential inhabits them.
            # check the prefix of the header

            # choose whether to look at the wsgi headers or use Flask request headers to get the Auth field
            if use_environ is None:
                auth = request.headers[auth_header]
            else:
                auth = use_environ[auth_header]

            # split the Authorization field into its parts
            space_idx = auth.find(" ")
            if space_idx != -1:
                auth_type_key = auth[0:space_idx].lower()
                auth_type_value = auth[space_idx+1:]
                extract_fn = None

                if auth_type_key == bearer_prefix.lower():
                    extract_fn = ServiceMiddleware._type_bearer
                elif auth_type_key == ldap_basic_prefix.lower():
                    extract_fn = ServiceMiddleware._type_ldap
                elif auth_type_key == aws_s3_rest_prefix.lower():
                    extract_fn = ServiceMiddleware._type_s3_rest
                elif auth_type_key == aws_v4_signed_prefix.lower():
                    extract_fn = ServiceMiddleware._type_v4_signature  # type: ignore

                if extract_fn:
                    user, password, hint = extract_fn(auth_credential_delimiter, auth_type_value)
                else:
                    # doesn't look like a recognized auth scheme that we deal with
                    root.warning(f"We cannot extract credentials for this type of authorization key {auth_type_key}")
            else:
                # doesn't look like an auth scheme
                pass

        if user is None:
            raise Unauthorized()

        return ServiceMiddleware._credentials_to_token(env, user, password, hint)

    @staticmethod
    def _credentials_to_token(env, user, password, hint):
        # we have this static method to make testing super easy to override
        return _pre_request_get_token(env, user, password, hint)

    @staticmethod
    def _split_to_jwt_or_credentials(
            auth_credential_delimiter, field_aws_access_key_id
    ) -> Tuple[str, str, Optional[str]]:
        if auth_credential_delimiter not in field_aws_access_key_id:
            # this MUST be a JWT, since there is no split character
            return field_aws_access_key_id, "NOP", "JWT"
        else:
            # we need to split into the respective values, split by the first we see
            # we still do not know which of the credential types it is however
            user, pasw = field_aws_access_key_id.split(auth_credential_delimiter, 1)
            return user, pasw, None

    @staticmethod
    def _type_ldap(auth_credential_delimiter, auth_type_value) -> Tuple[str, str, Optional[str]]:
        ldap_separator = ":"

        # only presto uses this, we know it is of the form (Basic <User>:<Password>) so we can split it
        # may be any one of the 3 credential types
        # we still do not know which of the credential types it is
        unencoded = base64.urlsafe_b64decode(auth_type_value).decode("ascii")
        user, pasw = unencoded.split(ldap_separator, 1)
        return user, pasw, None

    @staticmethod
    def _type_bearer(auth_credential_delimiter, auth_type_value) -> Tuple[str, str, Optional[str]]:
        # only datalake apps use bearer tokens, thus its a token of the form (Bearer <JWT>)
        # may only be JWT
        return auth_type_value, "NOP", "JWT"

    @staticmethod
    def _type_s3_rest(auth_credential_delimiter, auth_type_value) -> Tuple[str, str, Optional[str]]:
        aws_s3_rest_separator = ":"

        # only S3 REST, may be any one of the 3 credential types
        field_aws_access_key_id, _, _ = auth_type_value.strip().partition(aws_s3_rest_separator)
        return ServiceMiddleware._split_to_jwt_or_credentials(auth_credential_delimiter, field_aws_access_key_id)

    @staticmethod
    def _type_v4_signature(auth_credential_delimiter, auth_type_value) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        aws_v4_fields_separator = ","
        aws_v4_field_components_separator = "="
        aws_v4_credential_field = "Credential"
        aws_v4_credential_field_values_separator = "/"

        # only AWS V4 Signed use by s3proxy only, may be any one of the 3 credential types
        fields = auth_type_value.split(aws_v4_fields_separator)
        for field in fields:
            field_name, _, field_value = field.strip().partition(aws_v4_field_components_separator)

            if field_name == aws_v4_credential_field:
                field_aws_access_key_id, _, _ = field_value.partition(aws_v4_credential_field_values_separator)
                return ServiceMiddleware._split_to_jwt_or_credentials(auth_credential_delimiter, field_aws_access_key_id)

        # if Credential field is not in there, we need to return None, to hit Unauthorized
        return None, None, None