#  #
#  Copyright (C) 2020 IHS Markit.
#  All Rights Reserved
#  #
#

import logging
import socket
import os
import elasticache_auto_discovery
from pymemcache.client.hash import HashClient
from datetime import datetime, timedelta
from pymemcache import serde


logger = logging.getLogger(__name__)


def get_or_refresh_hashclient(func):
    def wrapper(self, *args, **kwargs):
        if not self._client or self._should_rediscover():
            self._rediscover_and_recreate_client_on_new_config()
        return func(self, *args, **kwargs)
    return wrapper


class RefreshingHashClient:
    def __init__(self, config):
        logger.debug('Init RefreshingHashClient', extra={'config': config})
        self.config = config
        self._client = None
        self._discovered_nodes = []
        self._last_successful_discovery = datetime.min

    @get_or_refresh_hashclient
    def get(self, key):
        try:
            logger.debug('refreshing_hashclient called GET', extra={'key': key})
            return self._client.get(key, None)
        except Exception:
            logging.exception('Exception calling cache GET', extra={'key': key})
            return None

    @get_or_refresh_hashclient
    def set(self, key, value, expire=0):
        try:
            logger.debug('refreshing_hashclient called SET', extra={'key': key, 'expire': expire})
            return self._client.set(key, value, expire=expire, noreply=False)
        except Exception:
            logging.exception('Exception calling cache SET', extra={'key': key})
            return None

    @get_or_refresh_hashclient
    def delete(self, key):
        try:
            logger.debug('refreshing_hashclient called DELETE', extra={'key': key})
            return self._client.delete(key, noreply=False)
        except Exception:
            logging.exception('Exception calling cache DELETE', extra={'key': key})
            return None

    def _rediscover_and_recreate_client_on_new_config(self):
        logger.debug('_rediscover_and_recreate_client_on_new_config')
        nodes = self._discover_nodes()
        if nodes and nodes != self._discovered_nodes:
            self._discovered_nodes = nodes
            logger.debug('create new HashClient within refreshing_hashclient')
            self._client = \
                HashClient(
                    servers=self._discovered_nodes,
                    use_pooling=True,
                    connect_timeout=self.config.time_to_timeout,
                    serde=serde.pickle_serde,
                )

    def _should_rediscover(self):
        now = datetime.utcnow()
        delta = timedelta(
            minutes=5.0
        )
        logger.debug(f"{now} - {self._last_successful_discovery} > {delta}")
        result = now - self._last_successful_discovery > delta
        logger.debug(
            f'_should_rediscover: {result}',
            extra={'now': now, '_last_successful_discovery': self._last_successful_discovery}
        )
        return result

    def _discover_nodes(self):
        logger.debug('_discover_nodes')
        # if running local you will not be able to reach EC memcache
        # but you must have a local memcache running (e.g. localhost:11211 - see /etc/memcached.conf)
        # start it with (sudo apt-get install memcached; sudo systemctl start/stop memcached)
        if os.environ.get('LOCAL_MEMCACHE', None):
            logger.warning(f"EC Memcache unreachable, connecting to local memcache {os.environ.get('LOCAL_MEMCACHE')}")
            self._last_successful_discovery = datetime.utcnow()
            return [os.environ.get('LOCAL_MEMCACHE').split(":")]

        try:
            nodes = elasticache_auto_discovery.discover(
                self.config.elasticache_config_node_url,
                time_to_timeout=self.config.time_to_timeout
            )
            self._last_successful_discovery = datetime.utcnow()
        except socket.timeout as e:
            logger.warning(f"Memcache is disabled because an exception occurred", exc_info=e)
            return None
        except Exception as e:
            logger.warning(f"Memcache is disabled because an exception occurred", exc_info=e)
            return None

        nodes = [
            (ip.decode("utf-8"), int(port)) for _server, ip, port in nodes
        ]

        logger.info(
            'elasticache_auto_discovery nodes',
            extra={
                'nodes': str(nodes),
                'num nodes': len(nodes),
                '_last_successful_discovery': self._last_successful_discovery,
            }
        )
        return nodes
