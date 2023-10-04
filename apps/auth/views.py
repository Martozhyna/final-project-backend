from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from apps.users.serializers import UserSerializer


class AuthRegisterView(CreateAPIView):
    """
    Register new user
    """
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


