from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView, get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from core.exceptions.jwt_exception import JWTException
from core.permissions.is_superuser import IsSuperuser
from core.services.email_service import EmailService
from core.services.jwt_service import ActivateToken, JWTService, PasswordRecoveryToken

from apps.auth.serializer import AuthPasswordSerializer
from apps.users.models import UserModel as User
from apps.users.serializers import UserSerializer

UserModel: User = get_user_model()


class AuthRegisterView(CreateAPIView):
    """
    Register new user
    """
    serializer_class = UserSerializer
    permission_classes = (IsSuperuser,)


class SendUserActivateTokenView(GenericAPIView):
    """
        Send activate token
    """

    queryset = UserModel.objects.all()
    permission_classes = (IsSuperuser,)

    def get(self, *args, **kwargs):
        user = self.get_object()
        token = JWTService.create_token(user, ActivateToken)
        url = f'http://localhost:3000/activate/{token}'
        EmailService.register_email(user, url)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)


class ActivateUserView(GenericAPIView):
    """
        Activate user
    """

    permission_classes = (AllowAny,)

    def post(self, *args, **kwargs):
        token = kwargs['token']
        try:
            user = JWTService.validate_token(token, ActivateToken)
        except JWTException:
            return Response({'error': 'посилання за яким ви перейшли - уже не існує'},
                            status=status.HTTP_400_BAD_REQUEST)
        user.is_active = True
        data = self.request.data
        serializer = AuthPasswordSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user.set_password(data['password'])
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


class PasswordRecoveryView(GenericAPIView):
    """
        Send token for recovery password
    """

    permission_classes = (IsSuperuser,)

    def post(self, *args, **kwargs):
        data = self.request.data
        try:
            validate_email(data.get('email', ''))
        except ValidationError:
            return Response({'error': 'Невірний формат email'}, status=status.HTTP_400_BAD_REQUEST)
        user = get_object_or_404(UserModel, email=data['email'])
        token = JWTService.create_token(user, PasswordRecoveryToken)
        url = f'http://localhost:3000/recovery-password/{token}'
        EmailService.password_recovery(user, url)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)


class PasswordChangeView(GenericAPIView):
    """
       Change password
    """

    def post(self, *args, **kwargs):
        token = kwargs['token']
        try:
            user = JWTService.validate_token(token, PasswordRecoveryToken)
        except JWTException:
            return Response({'error': 'посилання за яким ви перейшли - уже не існує'},
                            status=status.HTTP_400_BAD_REQUEST)
        data = self.request.data
        serializer = AuthPasswordSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user.set_password(data['password'])
        user.save()
        return Response('Пароль успішно змінено', status=status.HTTP_200_OK)
