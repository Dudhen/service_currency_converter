from django.urls import path

from currency_converter_app.api.views import ConverterCurrencyAPIView

app_name = 'currency_converter_app_api'

urlpatterns = [
    path('rates/', ConverterCurrencyAPIView.as_view(), name='rates'),
]
