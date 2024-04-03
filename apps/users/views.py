from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.views import APIView

from apps.orders.models import OrdersModel
from apps.orders.serializers import OrdersSerializers
from apps.users.serializers import UserSerializer

UserModel = get_user_model()


class UserMeView(ListAPIView):
    def get(self, *args, **kwargs):
        user = self.request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


class UsersListView(ListAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer


class UserOrdersStatisticView(APIView):
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