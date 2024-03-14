from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status

from apps.users.serializers import UserSerializer


class UserMeView(ListAPIView):
    def get(self, *args, **kwargs):
        user = self.request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)
