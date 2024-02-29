from django.db import models


class GroupsModel(models.Model):
    class Meta:
        db_table = 'groups'
        ordering = ('title',)

    title = models.CharField(max_length=20, unique=True)
