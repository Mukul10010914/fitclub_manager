# Generated by Django 3.2.8 on 2021-10-27 05:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0011_auto_20211027_1033'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='subscription',
        ),
    ]