# Generated by Django 2.1.15 on 2021-10-02 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gym_or_club', '0006_auto_20210921_1627'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='plan',
            field=models.CharField(choices=[('Free', 'Free'), ('Basic', 'Basic'), ('Premium', 'Premium')], default='Free', max_length=100),
        ),
    ]
