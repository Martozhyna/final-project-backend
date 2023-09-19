from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny

from apps.orders.models import OrdersModel
from apps.orders.serializers import OrdersSerializers


class OrdersListCreateView(ListCreateAPIView):
    # permission_classes = (AllowAny,)
    """
       Returns all orders. You can apply ordering to all fields and pagination
    """
    queryset = OrdersModel.objects.all()
    serializer_class = OrdersSerializers
    filter_backends = (OrderingFilter,)
    ordering_fields = ['id', 'name', 'surname', 'email', 'phone', 'age', 'course', 'course_format', 'course_type',
                       'status', 'sum', 'alreadyPaid', 'group', 'created_at', 'manager']


class OrdersRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """
      get:
          get order by id
      patch:
          partial update order by id
      put:
         full update order by id
      delete:
         delete order by id
    """
    queryset = OrdersModel.objects.all()
    serializer_class = OrdersSerializers
