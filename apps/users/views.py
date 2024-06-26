from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from core.permissions.is_superuser import IsSuperuser

from apps.orders.models import OrdersModel
from apps.orders.serializers import OrdersSerializers
from apps.users.serializers import UserSerializer

UserModel = get_user_model()


class UserMeView(ListAPIView):
    """
        Get me
    """

    def get(self, *args, **kwargs):
        user = self.request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


class UsersListView(ListAPIView):
    """
        Get all users
    """
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer


class UserOrdersStatisticView(APIView):
    """
        Get statistics of each user on the status of their own applications
    """
    serializer_class = OrdersSerializers

    def get(self, request, *args, **kwargs):
        users = UserModel.objects.all()
        statistics = {}

        for user in users:
            manager_surname = user.surname
            orders = OrdersModel.objects.filter(manager=manager_surname)
            user_id = user.id

            user_statistics = {
                'total': orders.count(),
                'agree': orders.filter(status='Agree').count(),
                'disagree': orders.filter(status='Disagree').count(),
                'in_work': orders.filter(status='In work').count(),
                'dubbing': orders.filter(status='Dubbing').count(),
                'new': orders.filter(status='New').count()
            }

            statistics[user_id] = user_statistics

        return Response({'statistics': statistics})


class UserBanView(GenericAPIView):
    """
        Ban user
    """
    queryset = UserModel.objects.all()
    permission_classes = (IsSuperuser,)

    def patch(self, *args, **kwargs):
        user = self.get_object()
        response_data = {}
        if user.is_staff:
            response_data[user.id] = {'error': 'ви не можете заблокувати самого себе'}
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        if user.is_active:
            user.is_active = False
            user.save()
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        response_data[user.id] = {'error': 'цей користувач уже заблокований'}
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


class UserUnbanView(GenericAPIView):
    """
        Unban user
    """
    queryset = UserModel.objects.all()
    permission_classes = (IsSuperuser,)

    def patch(self, *args, **kwargs):
        user = self.get_object()
        response_data = {}

        if user.is_staff:
            response_data[user.id] = {'error': 'ви не були заблоковані'}
        if user.is_active:
            response_data[user.id] = {'error': 'цей користувач уже розблокований'}
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        user.is_active = True
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

