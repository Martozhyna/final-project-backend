from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from core.services.jwt_service import ActivateToken, JWTService

from apps.auth.serializer import AuthPasswordSerializer
from apps.users.serializers import UserSerializer


class AuthRegisterView(CreateAPIView):
    """
    Register new user
    """
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class ActivateUserView(GenericAPIView):
    permission_classes = (AllowAny,)

    def get(self, *args, **kwargs):
        token = kwargs['token']
        user = JWTService.validate_token(token, ActivateToken)
        user.is_active = True
        data = self.request.data
        serializer = AuthPasswordSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user.set_password(data['password'])
        user.save()
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)
