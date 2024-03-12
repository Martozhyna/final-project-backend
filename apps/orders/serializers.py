from rest_framework import serializers

from apps.comments.serializers import CommentSerializer
from apps.orders.models import OrdersModel
from core.dataclasses.group_dataclass import Group


class GroupsRelatedFieldSerializer(serializers.RelatedField):
    def to_representation(self, value: Group):
        return {'id': value.id, 'title': value.title}


class GroupTitleSerializer(serializers.RelatedField):
    def to_representation(self, value):
        return value.title


class OrdersExelSerializer(serializers.ModelSerializer):
    group = GroupTitleSerializer(read_only=True)

    class Meta:
        model = OrdersModel
        fields = (
            'id', 'name', 'surname', 'email', 'phone', 'age', 'course', 'course_format', 'course_type', 'status', 'sum',
            'alreadyPaid', 'group', 'created_at', 'manager', 'utm', 'msg'
        )


class OrdersSerializers(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    group = GroupsRelatedFieldSerializer(read_only=True)

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
