from django.urls import path

from apps.orders.views import OrdersListCreateView, OrdersRetrieveUpdateDestroyView

urlpatterns = [
    path('', OrdersListCreateView.as_view(), name='orders_list_create'),
    path('/<int:pk>', OrdersRetrieveUpdateDestroyView.as_view(), name='orders_retrieve_update_destroy'),

]