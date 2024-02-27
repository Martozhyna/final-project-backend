from django.db import models


class GroupsModel(models.Model):
    class Meta:
        db_table = 'groups'

    title = models.CharField(max_length=20, unique=True)
