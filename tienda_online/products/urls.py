from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, ProductViewSet, PrecioFinalView

router = DefaultRouter()
router.register('products', ProductViewSet, basename='products')
router.register('categories', CategoryViewSet, basename='categories')

urlpatterns = [
    path('precio-final/', PrecioFinalView.as_view(), name='precio-final'),
    path('', include(router.urls)),
]
