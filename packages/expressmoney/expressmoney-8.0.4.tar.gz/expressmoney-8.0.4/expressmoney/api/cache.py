__all__ = ('CacheMixin', 'CacheObjectMixin')

import os
from typing import Union

from django.contrib.auth import get_user_model
from django.core.cache import cache

from expressmoney.api.utils import log

User = get_user_model()


class BaseCacheMixin:
    _cache_period: int = None

    @log
    def flush_cache(self):
        """Delete Redis cache for current endpoint"""
        self._memory_cache = None
        cache.delete(self._get_cache_key())

    @property
    def _cache(self):
        if self._memory_cache is None:
            try:
                cache_data = cache.get(self._get_cache_key())
                self._memory_cache = cache_data
                if os.getenv('IS_ENABLE_API_LOG') and cache_data is not None:
                    print(f'GET REDIS {self}')
            except ModuleNotFoundError:
                cache.set(self._get_cache_key(), None, None)
        return self._memory_cache

    @_cache.setter
    def _cache(self, value):
        if value is not None:
            cache.set(self._get_cache_key(), value, self._cache_period)
            self._memory_cache = value

    def _get_related_points(self) -> list:
        """Set related points here"""
        return list()

    def _flush_cache_related_points(self):
        related_points = self._get_related_points()
        for point in related_points:
            point.flush_cache()

    def _get_cache_key(self):
        generic_key = f'user{getattr(self._user, "id")}_{self._point_id.id}'
        suffix_params = self._cache_key_suffix_params
        key_with_params = generic_key if not suffix_params else f'{generic_key}{suffix_params}'
        if hasattr(self, '_pagination_pages') and self._pagination_pages is not None:
            key = f'{key_with_params}_pages{self._pagination_pages}'
        else:
            key = key_with_params
        return key

    @property
    def _cache_key_suffix_params(self):
        if self._query_params:
            suffix = ''
            for key, item in self._query_params.items():
                suffix += f'_{key}_{item}'
            return suffix


class GetCacheMixin:
    def _get(self, url) -> dict:
        if url is None and self._cache is not None:
            return self._cache
        return super()._get(url)


class CacheMixin(GetCacheMixin, BaseCacheMixin):

    def __init__(self,
                 user: User,
                 query_params: dict = None,
                 is_async: bool = False,
                 timeout: tuple = (30, 30)
                 ):
        super().__init__(user=user,
                         query_params=query_params,
                         is_async=is_async,
                         timeout=timeout,
                         )
        self._memory_cache = None
        self._payload = None

    def _post(self, payload: dict):
        self._payload = payload
        super()._post(payload)
        self._memory_cache = None
        self._flush_cache_related_points()

    def _post_file(self, file, file_name, type_):
        super()._post_file(file, file_name, type_)
        self._memory_cache = None
        self._flush_cache_related_points()


class CacheObjectMixin(GetCacheMixin, BaseCacheMixin):

    def __init__(self,
                 user: User,
                 lookup_field_value: Union[None, str, int] = None,
                 is_async: bool = False,
                 timeout: tuple = (30, 30)
                 ):
        super().__init__(user=user,
                         lookup_field_value=lookup_field_value,
                         is_async=is_async,
                         timeout=timeout
                         )
        self._memory_cache = None
        self._payload = None

    def _put(self, payload: dict):
        self._payload = payload
        super()._put(payload)
        self._memory_cache = None
        self._flush_cache_related_points()
