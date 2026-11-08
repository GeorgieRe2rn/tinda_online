from django.urls import path
from .views import CountriesSoapView

urlpatterns = [path('countries/', CountriesSoapView.as_view(), name='soap-countries')]
