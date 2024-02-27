from rest_framework.generics import ListCreateAPIView

from apps.groups.models import GroupsModel
from apps.groups.serializers import GroupsSerializer


class GroupsListCreateView(ListCreateAPIView):
    queryset = GroupsModel.objects.all()
    serializer_class = GroupsSerializer

