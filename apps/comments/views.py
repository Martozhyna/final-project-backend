from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView
from rest_framework.response import Response

from apps.comments.models import CommentModel
from apps.comments.serializers import CommentSerializer


class CommentListView(ListAPIView):
    """
       Return all comments
    """
    serializer_class = CommentSerializer
    queryset = CommentModel.objects.all()


