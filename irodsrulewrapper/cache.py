"""
This module contains CacheTTL class and initialize CacheTTL.CACHE_TIME_STOMP with CacheTTL.set_time_stomp().
"""

import time
import os


class CacheTTL:
    """
    This class has the basic functionalities for a Browser Cache Time To Live (TTL).

    Attributes
    ----------
    CACHE_TIME_STOMP: float
        Timestomp of the cache information last update.
    CACHE_USERS_GROUPS: dict[str: User|Group]
        Cached iRODS users and group information.
    """

    CACHE_TIME_STOMP = None
    CACHE_USERS_GROUPS = {}

    @classmethod
    def set_time_stomp(cls):
        cls.CACHE_TIME_STOMP = time.time()

    @classmethod
    def get_time_stomp(cls):
        return cls.CACHE_TIME_STOMP

    @classmethod
    def reset_time_stomp(cls):
        cls.CACHE_TIME_STOMP = time.time()

    @classmethod
    def check_if_cache_expired(cls):
        if time.time() >= cls.CACHE_TIME_STOMP + int(os.environ["CACHE_TTL_VALUE"]):
            cls.CACHE_USERS_GROUPS.clear()
            CacheTTL.reset_time_stomp()


CacheTTL.set_time_stomp()
