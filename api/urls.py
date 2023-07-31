# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import UsuarioViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),   # URL to obtain the token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),   # URL to refresh the token
    path('', include(router.urls)),
]
