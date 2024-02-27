from rest_framework.serializers import ModelSerializer, StringRelatedField

from apps.groups.models import GroupsModel
from apps.orders.serializers import OrdersSerializers


class GroupsSerializer(ModelSerializer):
    class Meta:
        model = GroupsModel
        fields = ('id', 'title', 'orders')
        read_only_fields = ('orders',)
