from django.urls import path

from .views import GroupsListCreateView

urlpatterns = [
    path('', GroupsListCreateView.as_view(), name='groups_list_create')

]