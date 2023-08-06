__all__ = ('OrderScoringPoint',)

from expressmoney.api import *


SERVICE = 'scoring'


class OrderScoringCreateContract(Contract):
    order_id = serializers.IntegerField(min_value=1)


class OrderScoringResponseContract(Contract):
    id = serializers.IntegerField(min_value=1)
    created = serializers.DateTimeField()
    score = serializers.DecimalField(max_digits=3, decimal_places=2)
    order_id = serializers.IntegerField(min_value=1)


class OrderScoringReadContract(OrderScoringResponseContract):
    pass


class OrderScoringID(ID):
    _service = SERVICE
    _app = 'credit_scoring'
    _view_set = 'order_scoring'


class OrderScoringPoint(ListPointMixin, ResponseMixin, CreatePointMixin, ContractPoint):
    _point_id = OrderScoringID()
    _read_contract = OrderScoringReadContract
    _create_contract = OrderScoringCreateContract
    _response_contract = OrderScoringResponseContract
