import time
import os


class CacheTTL:
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
