# from django.contrib.auth import get_user_model, login
#
# from rest_framework import permissions, status, views
# from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView, get_object_or_404
# from rest_framework.mixins import CreateModelMixin
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework.viewsets import GenericViewSet
#
# from apps.auth.serializer import EmailSerializer, LoginSerializer, PasswordSerializer
# from apps.users.serializers import UserSerializer
#
# UserModel = get_user_model()
#
#
# class AuthRegisterView(CreateAPIView):
#     model = get_user_model()
#     # queryset = UserModel.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = (AllowAny,)
#
#
# # class AuthLoginView(GenericAPIView):
# #     queryset = UserModel.objects.all()
# #     serializer_class = UserSerializer
#
# # def get(self, *args, **kwargs):
# #     data = self.request.data
# #     serializer = EmailSerializer(data=data)
# #     serializer.is_valid(raise_exception=True)
# #     url = 'http://localhost:8000/auth/login'
# #     response = requests.get(url, auth=HTTPBasicAuth('email', 'password'))
# #     user = get_object_or_404(UserModel, email=data['email'], password=response)
# #     print(response)
# #     print('111')
# #     orders = OrdersModel.objects.all()
# #     # password_serializer = PasswordSerializer(data=data)
# #     # password_serializer.is_valid(raise_exception=True)
# #     return Response(orders)
#
# # def get(self, *args, **kwargs):
# #     data = self.request.data
#
#
# class LoginView(APIView):
#     # This view should be accessible also for unauthenticated users.
#     permission_classes = (permissions.AllowAny,)
#
#     def get(self, request, format=None):
#         serializer = LoginSerializer(data=self.request.data,
#                                      context={'request': self.request})
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         login(request, user)
#         # orders = OrdersModel.objects.all()
#         # serializer_orders = OrdersSerializers(instance=orders, many=True)
#         return Response('ok', status=status.HTTP_202_ACCEPTED)
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from rest_framework_simplejwt.views import TokenObtainPairView

from apps.users.serializers import UserSerializer

from .serializer import TokenPairSerializer
from .swagger.decorators import auth_register_swagger, token_pair_swagger


@auth_register_swagger()
class AuthRegisterView(CreateAPIView):
    """
    Register new user
    """
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


@token_pair_swagger()
class TokenPairView(TokenObtainPairView):
    """
      Login user
    """
    serializer_class = TokenPairSerializer
