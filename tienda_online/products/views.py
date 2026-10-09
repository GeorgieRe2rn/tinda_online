from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework_simplejwt.authentication import JWTAuthentication
from .services import ProductPriceService


class PriceQuerySerializer(serializers.Serializer):
    product_id = serializers.IntegerField(min_value=1)


class PrecioFinalView(APIView):
    """Facade: una entrada HTTP para consultar y calcular el precio."""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = PriceQuerySerializer(data=request.query_params)
        query.is_valid(raise_exception=True)
        return Response(ProductPriceService.final_price(
            query.validated_data['product_id']
        ))

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
