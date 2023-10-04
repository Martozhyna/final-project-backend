from django.contrib.auth import get_user_model
from django.db import models

from apps.users.models import UserModel as User

UserModel: User = get_user_model()


class OrdersModel(models.Model):
    class Meta:
        db_table = 'orders'
        ordering = ('-id',)

    name = models.CharField(max_length=25, blank=True, null=True)
    surname = models.CharField(max_length=25, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=12, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    course = models.CharField(max_length=10, blank=True, null=True)
    course_format = models.CharField(max_length=15, blank=True, null=True)
    course_type = models.CharField(max_length=100, blank=True, null=True)
    sum = models.IntegerField(blank=True, null=True)
    alreadyPaid = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(max_length=6, blank=True, null=True)
    utm = models.CharField(max_length=100, blank=True, null=True)
    msg = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=15, blank=True, null=True)
    manager = models.CharField(max_length=20, blank=True, null=True)
    group = models.CharField(max_length=10, blank=True, null=True)
    user = models.ForeignKey(UserModel, on_delete=models.SET_NULL, blank=True, null=True, related_name='orders')

    def __str__(self):
        return self.manager
