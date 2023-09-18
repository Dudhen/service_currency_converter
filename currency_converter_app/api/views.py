from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import OpenApiResponse, extend_schema

from currency_converter_app.api.serializers import ConverterCurrencySerializer, CurrencyCheckDataSerializer
from currency_converter_app.api.utils import from_query, get_converted_currency


@extend_schema(
    summary='Конвертация валюты',
    description='Данное API конвертирует количество одной валюты в другую '
                '(Если значение value не передано - ставится значение по-умолчанию: 1)',
    responses={
        200: CurrencyCheckDataSerializer(),
        500: OpenApiResponse(description='Internal Server Error'),
    },
)
class ConverterCurrencyAPIView(APIView):
    """
    Представление для API конвертации валюты
    """
    serializer_class = ConverterCurrencySerializer
    permission_classes = (AllowAny,)
    http_method_names = ('get',)

    def get(self, request):
        value = self.request.GET.get('value')
        query_data = from_query(
            {
                'from_currency': self.request.GET.get('from'),
                'to_currency': self.request.GET.get('to'),
                'value': value if value else 1,
             },
            CurrencyCheckDataSerializer
        )
        result = get_converted_currency(query_data['from'], query_data['to'], query_data['value'])
        serializer = self.serializer_class(
            {
                'result': result,
            },
            context={
                'request': request,
            },
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
