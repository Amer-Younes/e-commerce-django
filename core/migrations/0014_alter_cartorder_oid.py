# Generated by Django 5.1.5 on 2025-02-25 01:32

import shortuuid.django_fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_cartorder_oid_alter_cartorder_sku'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartorder',
            name='oid',
            field=shortuuid.django_fields.ShortUUIDField(alphabet='1234567890', blank=True, length=5, max_length=20, null=True, prefix=''),
        ),
    ]
