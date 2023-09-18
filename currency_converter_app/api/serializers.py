from django.core.exceptions import ValidationError
from rest_framework import serializers

from currency_converter_app.api.utils import get_symbol_currency


class ConverterCurrencySerializer(serializers.Serializer):
    """Сеалайзер для валидации и отображения полученных результатов"""
    result = serializers.FloatField()


class CurrencyCheckDataSerializer(serializers.Serializer):
    """Сеалайзер для валидации переданных данных"""
    # Изменил 'from' на 'from_currency', и 'to' на 'to_currency' потому что 'from' - это занятое слово в python
    # query-параметры в ручке же остались как в ТЗ: 'from' и 'to'
    from_currency = serializers.CharField(source='from')
    to_currency = serializers.CharField(source='to')
    value = serializers.FloatField()

    def validate_from_currency(self, value):
        if get_symbol_currency(value):
            return value
        raise ValidationError('Валюты с таким кодом не существует')

    def validate_to_currency(self, value):
        if get_symbol_currency(value):
            return value
        raise ValidationError('Валюты с таким кодом не существует')
