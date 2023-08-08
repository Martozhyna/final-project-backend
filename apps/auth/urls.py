from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import AuthRegisterView, TokenPairView

urlpatterns = [

    path('/register', AuthRegisterView.as_view(), name='auth_register_user'),
    path('/login', TokenPairView.as_view(), name='auth_login'),
    path('/refresh', TokenRefreshView.as_view(), name='auth_refresh'),
]
