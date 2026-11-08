from django.conf import settings
from django.core.cache import cache
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from zeep import Client
from zeep.transports import Transport
import requests


class CountriesSoapView(APIView):
    """Consume la lista de países desde el CountryInfoService SOAP público."""
    permission_classes = [AllowAny]

    def get(self, request):
        countries = cache.get('soap-country-list')
        if countries is None:
            try:
                session = requests.Session()
                session.headers['User-Agent'] = 'TuntoOnline/1.0 (Django SOAP demo)'
                transport = Transport(session=session, timeout=12)
                client = Client(settings.SOAP_COUNTRIES_WSDL, transport=transport)
                countries = client.service.ListOfCountryNamesByName()
                countries = [{'code': item.sISOCode, 'name': item.sName} for item in countries]
                cache.set('soap-country-list', countries, 3600)
            except Exception as exc:
                return Response(
                    {'detail': 'No fue posible consultar el servicio SOAP público.', 'error': str(exc)},
                    status=502,
                )
        return Response({'source': 'SOAP CountryInfoService', 'count': len(countries), 'countries': countries})
