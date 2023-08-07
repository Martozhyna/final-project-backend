from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from apps.orders.models import OrdersModel
from apps.orders.serializers import OrdersSerializers


class OrdersListCreateView(ListCreateAPIView):
    queryset = OrdersModel.objects.all()
    serializer_class = OrdersSerializers
    filter_backends = (OrderingFilter,)
    ordering_fields = ['id', 'name', 'surname', 'email', 'phone', 'age', 'course', 'course_format', 'course_type',
                       'status', 'sum', 'alreadyPaid', 'group', 'created_at', 'manager']


class OrdersRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = OrdersModel.objects.all()
    serializer_class = OrdersSerializers
