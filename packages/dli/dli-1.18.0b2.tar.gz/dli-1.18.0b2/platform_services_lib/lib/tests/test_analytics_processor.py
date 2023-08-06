#
# Copyright (C) 2019 IHS Markit.
# All Rights Reserved
#

from mock import Mock

from ..services.analytics_service import AnalyticsService
from ..services.analytics_service.model import AnalyticsEvent


class TestAnalyticsProcessor:

    user_id = 'userId'
    identity_service = Mock()
    identity_service.dlc_me.return_value = {'datalake': {'user_id': user_id}}
    _analytics_processor = AnalyticsService(Mock(), identity_service)

    def test_process_action_returns_none_for_none_input(self):
        assert self._analytics_processor.process(None, user_id=self.user_id) is None

    def test_process_action_calls_analytics_service_methods(self):
        input = AnalyticsEvent(
            application_name='',
            application_version='',
            user_id='',
            entity='',
            action='',
            organisation_id='',
            result=1,
            properties={},
        )
        expected_body = 'body'
        self._analytics_processor._analytics_service.create_message_body = \
            Mock(return_value=expected_body)
        self._analytics_processor.process(action_info=input, user_id=self.user_id)

        self._analytics_processor._analytics_service.create_message_body \
            .assert_called_once_with(action_info=input, user_id=self.user_id)
        self._analytics_processor._analytics_service.send_message\
            .assert_called_once_with(expected_body)
