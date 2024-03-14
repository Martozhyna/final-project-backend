from django.urls import path

from apps.users.views import UserMeView

urlpatterns = [
    path('/me', UserMeView.as_view(), name='user_me_view')

]