# Generated by Django 4.2.5 on 2024-02-27 20:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_alter_ordersmodel_course_and_more'),
        ('comments', '0002_commentmodel_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentmodel',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comments', to='orders.ordersmodel'),
        ),
    ]