from django.urls import path

from apps.orders.views import OrderCreateListCommentsView, OrdersListCreateView, OrdersRetrieveUpdateDestroyView, \
    OrdersUserListView, OrdersExelTable

urlpatterns = [
    path('', OrdersListCreateView.as_view(), name='orders_list_create'),
    path('/<int:pk>', OrdersRetrieveUpdateDestroyView.as_view(), name='orders_retrieve_update_destroy'),
    path('/<int:pk>/comment', OrderCreateListCommentsView.as_view(), name='orders_create_list_comments'),
    path('/my', OrdersUserListView.as_view(), name='orders_user_list'),
    path('/exel', OrdersExelTable.as_view(), name='orders_exel_table')

]
