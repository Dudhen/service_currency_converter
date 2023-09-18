import typing

import requests
from currency_converter import CurrencyConverter
from forex_python.converter import CurrencyCodes
from rest_framework.serializers import Serializer


def from_query(
    data,
    serializer: type[Serializer],
    **kwargs: typing.Any,
) -> dict[str, typing.Any]:
    """
    Функция для валидации query-параметров сериалайзером
    """
    ser = serializer(data=data, **kwargs)
    ser.is_valid(raise_exception=True)
    return ser.validated_data


def get_converted_currency(
        from_currency: str,
        to_currency: str,
        value: int | float
) -> float:
    """
    Функция для конвертации переданного количества валюты
    в другую переданную валюту
    """
    url = f"https://currencies.apps.grandtrunk.net/getlatest/{from_currency}/{to_currency}"
    response = requests.get(url, timeout=10)
    result = response.json() * value

    # Изначально хотел использовать библиотеку currency_converter для конвертации (код ниже),
    # но вы написали "Данные о текущих курсах валют необходимо получать с внешнего сервиса",
    # и я решил, что использование библиотеки под это требование не подойдёт (тем более, она
    # перестала работать с рублями с мая 2022го года)

    # c = CurrencyConverter()
    # result = c.convert(value, from_currency, to_currency)
    return round(result, 2)


def get_symbol_currency(code: str) -> str:
    """
    Функция для получения символа валюты по коду
    """
    c = CurrencyCodes()
    return c.get_symbol(code)
