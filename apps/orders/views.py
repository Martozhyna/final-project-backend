import os
import tempfile

from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.response import Response
from django_filters import rest_framework as filters
import pandas as pd
from django.http import HttpResponse

from apps.comments.serializers import CommentSerializer
from apps.groups.models import GroupsModel
from apps.orders.filters import OrderFilter
from apps.orders.models import OrdersModel
from apps.orders.serializers import OrdersSerializers, OrdersExelSerializer
from apps.groups.serializers import GroupsSerializer


class OrdersListCreateView(ListCreateAPIView):
    """
    get:
          Returns all orders. You can apply ordering to all fields and pagination
    post:
          Create new orders
    """
    queryset = OrdersModel.objects.all()

    serializer_class = OrdersSerializers
    filterset_class = OrderFilter
    filter_backends = (OrderingFilter, filters.DjangoFilterBackend,)
    ordering_fields = ['id', 'name', 'surname', 'email', 'phone', 'age', 'course', 'course_format', 'course_type',
                       'status', 'sum', 'alreadyPaid', 'created_at', 'manager', 'group']

    def post(self, request, *args, **kwargs):
        data = self.request.data
        serializer = OrdersSerializers(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user, manager=self.request.user.surname)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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

    def patch(self, request, *args, **kwargs):
        order = self.get_object()  # Отримуємо екземпляр замовлення
        orders_user = order.manager  # хто є менеджером в заявці
        orders_manager = self.request.user.surname  # залогінений юзер
        group_title = request.data.get('group', False)  # група яку ми відправляємо
        serializer_group = GroupsSerializer

        if (not orders_user or orders_user == orders_manager) and group_title:
            try:
                group = GroupsModel.objects.get(
                    title=group_title)  # група яка є в списку і співпадає з тою, що ми відправляємо
                print(group.id)
                if group == order.group:
                    serializer = OrdersSerializers(order, data=request.data, partial=True)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                order.group = group
                order.save()
                # serializer = OrdersSerializers(order)
                serializer = OrdersSerializers(order, data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            except GroupsModel.DoesNotExist:
                # Якщо група не існує, повертаємо помилку і список наявних груп
                all_groups = GroupsModel.objects.all()
                serializer = serializer_group(all_groups, many=True)
                return Response({'error': 'Група не існує', 'available_groups': serializer.data},
                                status=status.HTTP_400_BAD_REQUEST)

        if (not orders_user or orders_user == orders_manager) and not group_title:
            serializer = OrdersSerializers(order, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            return Response('Ви не можете редагувати дану заявку', status=status.HTTP_400_BAD_REQUEST)


class OrderCreateListCommentsView(CreateAPIView):
    """
       get:
          get all comments by order id
       post:
          create new order's comment
    """
    queryset = OrdersModel.objects.all()
    serializer_class = CommentSerializer

    def post(self, request, *args, **kwargs):
        data = self.request.data
        order = self.get_object()
        orders_user = order.manager
        orders_manager = self.request.user.surname
        if not order.manager or orders_user == self.request.user.surname:
            serializer = CommentSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save(order=order)
            if not order.manager:
                order.manager = orders_manager
                order.save()
            if not order.status or order.status == 'New':
                order.status = 'In work'
                order.save()
            print(order.manager)
            print(self.request.user.surname)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(order.user)
            print(self.request.user.id)
            return Response('Ви не можете коментувати дану заявку', status=status.HTTP_400_BAD_REQUEST)

    def get(self, *args, **kwargs):
        order = self.get_object()
        serializer = self.serializer_class(order.comments, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class OrdersUserListView(ListAPIView):
    """
           get:
              get only my orders (with ordering, filter and pages)
    """
    queryset = OrdersModel.objects.all()
    serializer_class = OrdersSerializers
    filterset_class = OrderFilter
    filter_backends = (OrderingFilter, filters.DjangoFilterBackend,)
    ordering_fields = ['id', 'name', 'surname', 'email', 'phone', 'age', 'course', 'course_format', 'course_type',
                       'status', 'sum', 'alreadyPaid', 'created_at', 'manager', 'group']

    def get_queryset(self):
        orders_manager = self.request.user.surname
        return OrdersModel.objects.filter(manager=orders_manager)


class OrdersExelTable(ListAPIView):
    """
              get:
                 get exel tables
    """
    queryset = OrdersModel.objects.all()
    filterset_class = OrderFilter
    filter_backends = (OrderingFilter, filters.DjangoFilterBackend,)
    ordering_fields = ['id', 'name', 'surname', 'email', 'phone', 'age', 'course', 'course_format', 'course_type',
                       'status', 'sum', 'alreadyPaid', 'created_at', 'manager', 'group']

    def get(self, *args, **kwargs):
        orders = OrdersModel.objects.all()  # отримуємо всі заявки з бази даних
        serializer = OrdersExelSerializer(instance=orders, many=True)  # перетворюємо їх у формат JSON
        data = serializer.data  # усі змінені замовлення
        df = pd.DataFrame(data)  # робимо exel табличку
        temp_dir = tempfile.mkdtemp()  # cтворюємо тимчасовий каталог для збереження таблички
        excel_file_path = os.path.join(temp_dir, 'excel_file.xlsx')  # шлях до каталога
        df.to_excel(excel_file_path, index=False)  # записуємо дані в табличку без індексів
        with open(excel_file_path, 'rb') as excel_file:
            response = HttpResponse(excel_file.read(),
                                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=orders.xlsx'

        return response  # повертаємо HTTP-відповідь, яка буде містити Excel-файл, який користувач може завантажити з браузера
