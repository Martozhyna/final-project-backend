import os
import tempfile

from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.response import Response
from django_filters import rest_framework as filters
import pandas as pd
from django.http import HttpResponse
from django.db.models import Q
from datetime import datetime, timedelta

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


class OrdersExcelTable(ListAPIView):
    """
              get:
                 get exel tables
    """
    queryset = OrdersModel.objects.all()
    filterset_class = OrderFilter
    filter_backends = (OrderingFilter, filters.DjangoFilterBackend,)

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get('name')
        surname = self.request.query_params.get('surname')
        email = self.request.query_params.get('email')
        phone = self.request.query_params.get('phone')
        age = self.request.query_params.get('age')
        course = self.request.query_params.get('course')
        course_type = self.request.query_params.get('course_type')
        course_format = self.request.query_params.get('course_format')
        statuses = self.request.query_params.get('status')
        group = self.request.query_params.get('group')
        start_data = self.request.query_params.get('start_date')
        end_data = self.request.query_params.get('end_date')
        manager = self.request.query_params.get('manager')

        if course_type:
            queryset = queryset.filter(course_type=course_type)
        if course_format:
            queryset = queryset.filter(course_format=course_format)
        if name:
            queryset = queryset.filter(Q(name__icontains=name))
        if surname:
            queryset = queryset.filter(Q(surname__icontains=surname))
        if email:
            queryset = queryset.filter(Q(email__icontains=email))
        if phone:
            queryset = queryset.filter(Q(phone__icontains=phone))
        if age:
            queryset = queryset.filter(Q(age__icontains=age))
        if course:
            queryset = queryset.filter(course=course)
        if statuses:
            queryset = queryset.filter(status=statuses)
        if group:
            queryset = queryset.filter(group=group)
        if start_data:
            start_date = datetime.strptime(start_data, '%Y-%m-%d')
            queryset = queryset.filter(created_at__gte=start_date)
        if end_data:
            end_date = datetime.strptime(end_data, '%Y-%m-%d') + timedelta(days=1)
            queryset = queryset.filter(created_at__lt=end_date)
        if manager:
            queryset = queryset.filter(manager=manager)

        return queryset

    def get(self, *args, **kwargs):
        orders = self.get_queryset()
        serializer = OrdersExelSerializer(instance=orders, many=True)
        data = serializer.data
        df = pd.DataFrame(data)
        temp_dir = tempfile.mkdtemp()
        excel_file_path = os.path.join(temp_dir, 'excel_file.xlsx')
        df.to_excel(excel_file_path, index=False)
        with open(excel_file_path, 'rb') as excel_file:
            response = HttpResponse(excel_file.read(),
                                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=orders.xlsx'

        return response


class OrdersStatusStatisticView(ListAPIView):
    queryset = OrdersModel.objects.all()
    serializer_class = OrdersSerializers

    def get(self, request, *args, **kwargs):
        data = OrdersModel.objects.all()
        params_dict = self.request.query_params.dict()

        order_statistic = []
        total = len(data)
        agree = 0
        in_work = 0
        disagree = 0
        dubbing = 0
        new = 0
        for i in data:
            if i.status == 'Agree':
                agree += 1
            if i.status == 'In work':
                in_work += 1
            if i.status == 'Disagree':
                disagree += 1
            if i.status == 'Dubbing':
                dubbing += 1
            if i.status == 'New':
                new += 1
        order_statistic.append(
            {'Total': total, 'Agree': agree, 'Disagree': disagree, 'In work': in_work, 'Dubbing': dubbing, 'New': new})

        return Response(order_statistic)
