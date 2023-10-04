from rest_framework import serializers

from apps.comments.models import CommentModel


class CommentSerializer(serializers.ModelSerializer):
    order = serializers.StringRelatedField()

    class Meta:
        model = CommentModel
        fields = ('id', 'comment', 'created_at', 'order')
