from rest_framework import serializers

from apps.comments.serializers import CommentSerializer
from apps.orders.models import OrdersModel
from apps.users.serializers import UserSerializer


class OrdersSerializers(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = OrdersModel
        fields = (
            'id', 'name', 'surname', 'email', 'phone', 'age', 'course', 'course_format', 'course_type', 'status', 'sum',
            'alreadyPaid', 'group', 'created_at', 'manager', 'utm', 'msg', 'comments', 'user')
        read_only_fields = ('user',)


class OrderManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdersModel
        fields = ('manager',)
