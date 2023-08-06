import operator
import os
from unittest import mock

import jwt
import pytest
from pymemcache.test.utils import MockMemcacheClient

from ..providers.memcache_provider import memcached_method

@mock.patch.dict(os.environ, {"JWT_SECRET_KEY": "secret"})
def test_cached_method(platform_app_blueprint):

    class T:
        cache = MockMemcacheClient()

        @memcached_method(
            cache_getter=operator.attrgetter('cache'),
            key=lambda *args: '123',
            cache_func_name='list_objects_v2',
        )
        def method(self, a):
            return 1

    assert T().method(None) == 1

    # Will only be one key
    key = next(iter(T.cache._contents.keys()))

    assert T.cache.get(key) == 1
    assert T.cache.set(key, 2)
    assert T().method(None) == 2


@mock.patch.dict(os.environ, {"JWT_SECRET_KEY": "secret"})
def test_cache_method_jwt_is_converted_to_sub(platform_app_blueprint):

    class T:
        cache = MockMemcacheClient()
        method_call_count = {}

        @memcached_method(
            cache_getter=operator.attrgetter('cache'),
        )
        def method(self, jwt: str, organisation_shortcode: str):
            if not T.method_call_count.get(jwt, False):
                T.method_call_count[jwt] = 0

            T.method_call_count[jwt] += 1
            return jwt

    # make sure a bad jwt ends up in the cache/makes real call with jwt untouched
    jwt_without_sub = jwt.encode(payload={"some": "payload"}, key="secret", algorithm="HS256")
    clazz = T()
    r = clazz.method(jwt=str(jwt_without_sub), organisation_shortcode="IHSMarkit")
    assert T.method_call_count[jwt_without_sub] == 1
    assert r == jwt_without_sub

    # should still call real method with jwt untouched
    jwt_with_sub = jwt.encode(payload={"some": "payload", "sub": "timothy@ihsmarkit"}, key="secret", algorithm="HS256")
    r2 = clazz.method(jwt=str(jwt_with_sub), organisation_shortcode="IHSMarkit")
    assert T.method_call_count[jwt_with_sub] == 1
    assert r2 == jwt_with_sub

    # now cached with sub, should use cached value not make real call with same jwt
    r3 = clazz.method(jwt=str(jwt_with_sub), organisation_shortcode="IHSMarkit")
    assert T.method_call_count[jwt_with_sub] == 1
    assert r3.decode() == jwt_with_sub

    # now cached with sub, should use cached value not make real call with another jwt (same sub)
    another_jwt_with_sub = jwt.encode(payload={"some": "payload 2 - is different see", "sub": "timothy@ihsmarkit"}, key="secret", algorithm="HS256")
    assert jwt_with_sub != another_jwt_with_sub
    r4 = clazz.method(jwt=str(another_jwt_with_sub), organisation_shortcode="IHSMarkit")
    with pytest.raises(KeyError):
        # not present in cache, as receives result of r2
        _ = T.method_call_count[r4]

    assert len(T.method_call_count) == 2
    assert r4.decode() == r2

    # now cached with sub, but different args to method, check additional call made
    r5 = clazz.method(jwt=str(another_jwt_with_sub), organisation_shortcode="S&PGlobal")
    assert len(T.method_call_count) == 3
