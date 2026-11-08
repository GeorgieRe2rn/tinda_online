from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .views import MeView, RegisterView, UserViewSet
from .serializers import EmailTokenObtainPairSerializer


class EmailTokenView(APIView):
    """Issue access and refresh JWTs using an email address and password."""
    permission_classes = []

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'password'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, format='email'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, format='password'),
            },
        ),
        responses={200: openapi.Response('Tokens JWT', schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={'access': openapi.Schema(type=openapi.TYPE_STRING), 'refresh': openapi.Schema(type=openapi.TYPE_STRING)},
        ))},
    )
    def post(self, request):
        serializer = EmailTokenObtainPairSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')

urlpatterns = [
    path('auth/me/', MeView.as_view(), name='user-me'),
    path('auth/register/', RegisterView.as_view(), name='user-register'),
    path('auth/token/', EmailTokenView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]
