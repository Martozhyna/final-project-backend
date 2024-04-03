from django.urls import path

from apps.users.views import UserMeView, UsersListView, UserOrdersStatisticView

urlpatterns = [
    path('/me', UserMeView.as_view(), name='user_me_view'),
    path('', UsersListView.as_view(), name='user_list_view'),
    path('/statistics', UserOrdersStatisticView.as_view(), name='user_order_status_statistics')

]