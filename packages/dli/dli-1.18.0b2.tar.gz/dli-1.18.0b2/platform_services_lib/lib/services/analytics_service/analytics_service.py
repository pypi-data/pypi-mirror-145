#
# Copyright (C) 2019 IHS Markit.
# All Rights Reserved
#
from ..cached_fetcher_service import CachedFetcherService
from ...providers.oidc_provider import JWTEncoded

try:
    # these are only present for services, not for the SDK, and we do not wish to impose these in requirements.txt
    from injector import inject
except ModuleNotFoundError:
    # set up an Identity decorator for @inject
    def inject(function):  # type: ignore
        def wrapper(*args, **kwargs):
            return function(*args, *kwargs)
        return wrapper
except:
    pass

from ..analytics_service.model import AnalyticsEvent
from ..ga_service.ga_service import GoogleAnalyticsService
import logging

logger = logging.getLogger(__name__)


class AnalyticsService:

    @inject
    def __init__(
        self,
        analytics_service: GoogleAnalyticsService,
        identity_service: CachedFetcherService,
    ):
        logger.debug('Init AnalyticsService')
        self._analytics_service = analytics_service
        self.identity_service = identity_service

    def map_jwt_to_user_id(self) -> str:
        """
        Lookup user_id for this user using the JWT. This is so that we do not leak user email addresses in either
        Google Analytics (which is against the Google terms of service) or DataDog.

        Returns: user_id from Catalogue
        """

        # Identity needs the encoded token! If you pass the decoded token then you will get an empty dict back from /me.
        from flask import current_app
        jwt_encoded: JWTEncoded = current_app.injector.get(JWTEncoded)

        me = self.identity_service.dlc_me(jwt=jwt_encoded)

        if me and 'datalake' in me and 'user_id' in me['datalake']:
            user_id = me['datalake']['user_id']
        else:
            logger.warning(
                'For some reason we could not get the user id for the JWT',
                extra={'me': me}
            )
            user_id = 'missing'

        return user_id

    def process(self, action_info: AnalyticsEvent, user_id: str) -> None:
        if not action_info:
            return

        body = self._analytics_service.create_message_body(action_info=action_info, user_id=user_id)
        self._analytics_service.send_message(body)
