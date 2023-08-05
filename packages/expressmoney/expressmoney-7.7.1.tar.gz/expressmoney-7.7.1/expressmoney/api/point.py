"""
Endpoints handlers
"""

__all__ = ('PointRequestError', 'PointServerError', 'PointClientError', 'PointNotFound404', 'PointThrottled',
           'Point', 'ObjectPoint', 'ContractPoint', 'ContractObjectPoint',
           'ListPointMixin', 'RetrievePointMixin', 'ResponseMixin', 'CreatePointMixin', 'UpdatePointMixin',
           'UploadFilePointMixin', 'ActionPointMixin',
           'ID', 'Contract', 'PaginationContract'
           )

from typing import OrderedDict, Union

from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

from expressmoney import status
from expressmoney.api.cache import CacheMixin, CacheObjectMixin
from expressmoney.api.contract import Contract, PaginationContract
from expressmoney.api.filter import FilterMixin
from expressmoney.api.id import ID
from expressmoney.api.utils import log
from expressmoney.api.client import Request, Tasks


User = get_user_model()


class PointError(Exception):
    pass


class SyncOnly(PointError):
    pass


class LookupFieldValueNone(PointError):
    pass


class SortByNotSet(PointError):
    pass


class ContractNotSet(PointError):
    pass


class PointRequestError(PointError):
    default_url = None
    default_status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'A server error occurred.'

    def __init__(self, url=None, status_code=None, detail=None):
        self.__url = self.default_url if url is None else url
        self.__status_code = self.default_status_code if status_code is None else status_code
        self.__detail = self.default_detail if detail is None else detail

    @property
    def url(self):
        return self.__url

    @property
    def status_code(self):
        return self.__status_code

    @property
    def detail(self):
        return self.__detail


class PointServerError(PointRequestError):
    pass


class PointClientError(PointRequestError):
    default_status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Invalid payload.'


class PointNotFound404(PointClientError):
    default_status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Not found'


class PointThrottled(PointClientError):
    default_status_code = status.HTTP_429_TOO_MANY_REQUESTS
    default_detail = None


class Point:
    """Base endpoint handler"""
    _point_id: ID = None

    @log
    def __init__(self, user: User, is_async: bool = False, timeout: tuple = (30, 30)):
        self._user = user
        self._cache = None
        self._response = None
        self._is_async = is_async
        self._client = (Request(service=self._point_id.service,
                                path=self._path,
                                user=user,
                                timeout=timeout,
                                ) if not is_async else
                        Tasks(service=self._point_id.service,
                              path=self._path,
                              user=user,
                              )
                        )

    @property
    def _path(self):
        path = self._point_id.path
        return path

    def _post(self, payload: dict):
        self._response = self._client.post(payload=payload)
        self._handle_error(self._response)

    @log
    def _get(self) -> dict:
        self._response = self._client.get()
        self._handle_error(self._response)
        data = self._response.json()
        return data

    def _post_file(self, file, file_name, type_):
        if self._is_async:
            raise SyncOnly('Post file allowed only for sync request.')
        self._response = self._client.post_file(file=file, file_name=file_name, type_=type_)
        self._handle_error(self._response)

    def _handle_error(self, response):
        if not self._is_async:
            if not status.is_success(response.status_code):
                if status.is_client_error(response.status_code):
                    if status.is_not_found(response.status_code):
                        self._cache = status.HTTP_404_NOT_FOUND
                        raise PointNotFound404(self._point_id.url)
                    if response.status_code == status.HTTP_429_TOO_MANY_REQUESTS:
                        raise PointThrottled(self._point_id.url, response.status_code, response.headers.get(
                            'Retry-After'))
                    else:
                        raise PointClientError(self._point_id.url, response.status_code, response.json())
                else:
                    raise PointServerError(self._point_id.url, response.status_code, response.text)


class ObjectPoint(Point):
    """For one object endpoints"""

    def __init__(self,
                 user: User,
                 lookup_field_value: Union[None, str, int] = None,
                 is_async: bool = False,
                 timeout: tuple = (30, 30),
                 ):
        if lookup_field_value is None:
            raise LookupFieldValueNone('lookup_field_value not filled')
        self._lookup_field_value = lookup_field_value
        self._point_id.lookup_field_value = lookup_field_value
        super().__init__(user, is_async, timeout)

    def _put(self, payload: dict):
        self._response = self._client.put(payload=payload)
        self._handle_error(self._response)


class ContractPoint(FilterMixin, CacheMixin, Point):
    """Endpoints with validated data by contract"""
    _read_contract = None
    _create_contract = None
    _sort_by = 'id'

    @property
    def _sorted_data(self) -> tuple:
        if self._sort_by is None:
            raise SortByNotSet('Set key for sort or False')
        validated_data = self._get_validated_data()
        sorted_data = sorted(validated_data, key=lambda obj: obj[self._sort_by]) if self._sort_by else validated_data
        return tuple(sorted_data)

    def _get_validated_data(self):
        data = self._handle_pagination(self._get())
        contract = self._get_contract(data, True)
        validated_data = contract.validated_data
        if self._cache is None:
            self._cache = validated_data
        return validated_data

    def _get_contract(self, data, is_read: bool) -> Contract:
        contract_class = self.__get_contract_class(is_read)
        contract = contract_class(data=data, many=True if is_read else False)
        self.__validate_contract(contract)
        return contract

    def __get_contract_class(self, is_read: bool):
        return self._read_contract if is_read else self._create_contract

    def __validate_contract(self, contract):
        try:
            contract.is_valid(raise_exception=True)
        except ValidationError as e:
            self.flush_cache()
            raise ValidationError(e.detail)

    @staticmethod
    def _handle_pagination(data):
        """Get current page and link on next page"""
        if isinstance(data, list) or None in (data.get('count'), data.get('results')):
            return data
        pagination = {
            'previous': data.get('previous'),
            'next': data.get('next'),
            'count': data.get('count'),
        }
        data = data.get('results')
        data = [dict(**entity, pagination=pagination) for entity in data]
        return data


class ContractObjectPoint(CacheObjectMixin, ObjectPoint):
    """Endpoints for one object with validated data by contract"""
    _read_contract = None
    _update_contract = None

    def _get_validated_data(self):
        data = self._get()
        if status.is_not_found(data):
            raise PointNotFound404
        contract = self._get_contract(data, True)
        validated_data = contract.validated_data
        if self._cache is None:
            self._cache = validated_data
        return validated_data

    def _get_contract(self, data, is_read: bool) -> Contract:
        contract_class = self.__get_contract_class(is_read)
        contract = contract_class(data=data, many=False)
        self.__validate_contract(contract)
        return contract

    def __get_contract_class(self, is_read: bool):
        return self._read_contract if is_read else self._update_contract

    def __validate_contract(self, contract):
        try:
            contract.is_valid(raise_exception=True)
        except ValidationError as e:
            self.flush_cache()
            raise ValidationError(e.detail)


class ListPointMixin:
    """For type ContractPoint"""

    def list(self) -> tuple:
        if self._read_contract is None:
            raise ContractNotSet(f'Set attr read_contract')
        return self._sorted_data


class RetrievePointMixin:
    """For type ContractObjectPoint"""

    def retrieve(self) -> OrderedDict:
        if self._read_contract is None:
            raise ContractNotSet(f'Set attr read_contract')
        return self._get_validated_data()


class CreatePointMixin:
    """For type ContractPoint"""

    def create(self, payload: dict):
        if self._create_contract is None:
            raise ContractNotSet(f'Set attr create_contract')
        contract = self._get_contract(data=payload, is_read=False)
        self._post(contract.data)


class UpdatePointMixin:
    """For type ContractObjectPoint"""

    def update(self, payload: dict):
        if self._update_contract is None:
            raise ContractNotSet(f'Set attr update_contract')

        contract = self._get_contract(data=payload, is_read=False)
        self._put(contract.validated_data)


class ResponseMixin:
    """Only for create and update actions"""

    _response_contract = None

    @property
    def response(self) -> OrderedDict:
        if self._response_contract is None:
            raise ContractNotSet('Response contract not set')
        if self._response is None:
            raise PointError('First create or update data')
        if self._response.status_code != status.HTTP_201_CREATED:
            raise PointError(f'Response data only for 201 status, current {self._response.status_code}')
        contract = self._response_contract(data=self._response.json())
        contract.is_valid(raise_exception=True)
        return contract.validated_data


class UploadFilePointMixin:
    """For any type Point"""

    def upload_file(self, file, filename: str, file_type: int):
        self._post_file(file, filename, file_type)


class ActionPointMixin:
    """For any type Point"""

    def action(self):
        self._get()
