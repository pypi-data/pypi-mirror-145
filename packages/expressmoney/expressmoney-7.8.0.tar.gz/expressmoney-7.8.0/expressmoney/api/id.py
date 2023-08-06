"""
 Microservice endpoint identifier
"""
__all__ = ('ID',)

from typing import Union


class ID:
    """Base microservice endpoint identifier"""
    _service = None
    _app = None
    _view_set = None
    _action = None

    def __init__(self):
        self._lookup_field_value = None
        super().__init__()

    @property
    def id(self):
        result = f'{self.service}_{self._app}_{self._view_set}'
        result = result if self._lookup_field_value is None else f'{result}_{self._lookup_field_value}'
        result = result if self._action is None else f'{result}_{self._action}'
        return result

    @property
    def service(self):
        return self._service

    @property
    def path(self):
        result = f'/{self._app}' if self._view_set is None else f'/{self._app}/{self._view_set}'
        result = result if self._lookup_field_value is None else f'{result}/{self._lookup_field_value}'
        result = result if self._action is None else f'{result}/{self._action}'
        return result

    @property
    def url(self):
        return f'https://{self.service}.expressmoney.com{self.path}'

    @property
    def lookup_field_value(self):
        return self._lookup_field_value

    @lookup_field_value.setter
    def lookup_field_value(self, value):
        self._lookup_field_value = value
