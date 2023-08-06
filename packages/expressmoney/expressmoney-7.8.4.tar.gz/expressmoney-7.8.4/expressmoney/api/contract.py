__all__ = ('Contract', 'PaginationContract')

from rest_framework import serializers


class ContractError(serializers.ValidationError):
    pass


class Contract(serializers.Serializer):

    def is_valid(self, raise_exception=False):
        try:
            return super().is_valid(raise_exception)
        except serializers.ValidationError as e:
            raise ContractError(e.detail)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class PaginationContract(Contract):
    previous = serializers.URLField(allow_null=True)
    next = serializers.URLField(allow_null=True)
    count = serializers.IntegerField()
