from django_filters import rest_framework as filters
from django_filters.widgets import RangeWidget
from django_filters.fields import DateRangeField

from apps.orders.models import OrdersModel


class DateRangeFilter(filters.Filter):
    field_class = DateRangeField
    widget = RangeWidget


class OrderFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    surname = filters.CharFilter(field_name='surname', lookup_expr='icontains')
    email = filters.CharFilter(field_name='email', lookup_expr='icontains')
    phone = filters.NumberFilter(field_name='phone', lookup_expr='icontains')
    age = filters.NumberFilter(field_name='age', lookup_expr='icontains')
    course = filters.TypedChoiceFilter(field_name='course', choices=[
        ('FS', 'FS'),
        ('QACX', 'QACX'),
        ('JCX', 'JCX'),
        ('JSCX', 'JSCX'),
        ('FE', 'FE'),
        ('PCX', 'PCX'),
    ], coerce=str)
    course_format = filters.TypedChoiceFilter(field_name='course_format', choices=[
        ('static', 'static'),
        ('online', 'online')
    ], coerce=str)
    course_type = filters.TypedChoiceFilter(field_name='course_type', choices=[
        ('pro', 'pro'),
        ('minimal', 'minimal'),
        ('premium', 'premium'),
        ('incubator', 'incubator'),
        ('vip', 'vip')
    ], coerce=str)
    status = filters.TypedChoiceFilter(field_name='status', choices=[
        ('In work', 'In work'),
        ('New', 'New'),
        ('Agree', 'Agree'),
        ('Disagree', 'Disagree'),
        ('Dubbing', 'Dubbing'),
    ], coerce=str)
    group = filters.CharFilter(field_name='group__title', lookup_expr='icontains')
    start_date = filters.DateFilter(field_name='created_at', lookup_expr='date__gt')
    end_date = filters.DateFilter(field_name='created_at', lookup_expr='date__lte')
    manager = filters.CharFilter(field_name='manager', lookup_expr='contains')



    class Meta:
        model = OrdersModel
        fields = ('name', 'surname', 'email', 'phone', 'age', 'course',
                  'course_format', 'course_type', 'status', 'group', 'start_date', 'end_date', 'manager')
