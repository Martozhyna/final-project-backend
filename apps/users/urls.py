from django.urls import path

from apps.users.views import UserMeView, UsersListView, UserOrdersStatisticView, UserBanView, UserUnbanView

urlpatterns = [
    path('/me', UserMeView.as_view(), name='user_me_view'),
    path('', UsersListView.as_view(), name='user_list_view'),
    path('/statistics', UserOrdersStatisticView.as_view(), name='user_order_status_statistics'),
    path('/<int:pk>/ban', UserBanView.as_view(), name='user_ban'),
    path('/<int:pk>/unban', UserUnbanView.as_view(), name='user_unban'),

]