# Generated by Django 5.1.5 on 2025-02-25 01:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0004_alter_contactus_options_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pics/'),
        ),
    ]
