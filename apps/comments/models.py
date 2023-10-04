from django.db import models

from apps.orders.models import OrdersModel


class CommentModel(models.Model):
    class Meta:
        db_table = 'comments'
        ordering = ('id',)

    comment = models.CharField(max_length=100)
    order = models.ForeignKey(OrdersModel, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
