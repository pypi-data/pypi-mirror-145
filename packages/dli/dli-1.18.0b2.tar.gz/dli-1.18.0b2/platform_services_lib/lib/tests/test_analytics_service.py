#
# Copyright (C) 2019 IHS Markit.
# All Rights Reserved
#
import pytest
import requests
from mock import Mock

from ..services.analytics_service.model import AnalyticsEvent
from ..services.ga_service import GoogleAnalyticsService


class TestAnalyticsService:

    user_id = 'userId'
    tracking_id = 'UA-123456-7'
    identity_service = Mock()
    identity_service.dlc_me.return_value = {'datalake': {'user_id': user_id}}
    analytics_service = GoogleAnalyticsService(
        ga_client=Mock(),
        config=Mock(tracking_id=tracking_id, ga_request_timeout=60),
    )

    # Stub the GET identity/me endpoint.
    identity_service.me = lambda jwt: {'datalake': {'user_id': 'userId'}}

    def test_uses_tracking_id_from_config(self):
        assert self.analytics_service._config.tracking_id == self.tracking_id

    def test_sends_post_with_specified_body_to_specified_url(self):
        body = 'body'
        self.analytics_service.send_message(body)

        self.analytics_service._ga_client.post.assert_called_with(
            '', data=body, timeout=60,
        )

    def test_creates_body_based_on_action_event(self, platform_app_blueprint):
        action_info = AnalyticsEvent(**{
            'application_name': 'someName',
            'application_version': 'someVersion',
            'user_id': 'userId',
            'organisation_id': 'organisationId',
            'entity': 'entityName',
            'action': 'actionName',
            'properties': {'package_id': 123, 'dataset_id': 456},
            'result': 'finalResult'
        })
        result = self.analytics_service.create_message_body(action_info, self.user_id)

        assert result == (
            'v=1&tid=UA-123456-7&t=event&an=someName&av=someVersion&'
            'cid=userId&ec=entityName&ea=actionName&ev=finalResult&'
            'cd1=userId&cd9=userId&cd2=organisationId&cd3=123&cd4=456'
        )

    def test_creates_body_based_on_action_event_missing_some_basic_data(self, platform_app_blueprint):
        action_info = AnalyticsEvent(**{
            'application_name': 'someName',
            'application_version': 'someVersion',
            'user_id': 'userId',
            'organisation_id': 'organisationId',
            'entity': 'entityName',
            'properties': {'package_id': 123, 'dataset_id': 456},
        })
        result = self.analytics_service.create_message_body(action_info, self.user_id)

        assert result == (
            'v=1&tid=UA-123456-7&t=event&an=someName&av=someVersion&'
            'cid=userId&ec=entityName&cd1=userId&cd9=userId&cd2=organisationId&'
            'cd3=123&cd4=456'
        )

    def test_creates_body_based_on_action_event_missing_some_properties(self, platform_app_blueprint):
        action_info = AnalyticsEvent(**{
            'application_name': 'someName',
            'application_version': 'someVersion',
            'user_id': 'userId',
            'organisation_id': 'organisationId',
            'entity': 'entityName',
            'properties': {'dataset_id': 456},
        })
        result = self.analytics_service.create_message_body(action_info, self.user_id)

        assert result == (
            'v=1&tid=UA-123456-7&t=event&an=someName&av=someVersion&'
            'cid=userId&ec=entityName&cd1=userId&cd9=userId&cd2=organisationId&cd4=456'
        )

    def test_creates_body_without_properties(self, platform_app_blueprint):
        action_info = AnalyticsEvent(**{
            'application_name': 'someName',
            'application_version': 'someVersion',
            'user_id': 'userId',
            'entity': 'entityName'
        })

        result = self.analytics_service.create_message_body(action_info, self.user_id)

        assert result == (
            'v=1&tid=UA-123456-7&t=event&an=someName&av=someVersion&'
            'cid=userId&ec=entityName&cd1=userId&cd9=userId'
        )

    def test_raise_when_sends_message_raises_unhandled_exception(self):
        self.analytics_service.logger.exception = Mock()
        ex = Exception('Test')
        self.analytics_service._ga_client.post.side_effect = Mock(
            side_effect=ex
        )

        body = 'body'
        self.analytics_service.send_message(body)

        self.analytics_service._ga_client.post.assert_called_with(
            '', data=body, timeout=60,
        )
        self.analytics_service.logger.exception.assert_called_with(
            self.analytics_service.ga_unhandled_exception_message
        )

    @pytest.mark.parametrize("exception,message", [
        [ConnectionResetError('Test'), 'GA ConnectionResetError'],
        [ConnectionAbortedError('Test'), 'GA ConnectionAbortedError'],
        [
            requests.exceptions.ConnectionError('Test'),
            'GA ConnectionError connection aborted'
        ],
    ])
    def test_catches_when_sends_message_raises_connection_error(
            self,
            exception,
            message
    ):
        self.analytics_service.logger.warning = Mock()
        self.analytics_service._ga_client.post.side_effect = Mock(
            side_effect=exception
        )

        body = 'body'
        self.analytics_service.send_message(body)

        self.analytics_service.logger.warning.assert_called_with(
            message, exc_info=exception,
        )
