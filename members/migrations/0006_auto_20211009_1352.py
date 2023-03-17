# Generated by Django 2.1.15 on 2021-10-09 08:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0005_client_profile_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='client_membership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan', models.CharField(blank=True, choices=[('Monthly', 'Monthly'), ('Quaterly', 'Quaterly'), ('Yearly', 'Yearly')], max_length=100)),
                ('due_date', models.DateField(blank=True, default=None)),
                ('amount', models.CharField(blank=True, max_length=100)),
                ('payment_method', models.CharField(blank=True, choices=[('Cash', 'Cash'), ('Online Payment', 'Online Payment')], max_length=100)),
                ('paid', models.BooleanField(default=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='client',
            name='amount',
        ),
        migrations.RemoveField(
            model_name='client',
            name='due_date',
        ),
        migrations.RemoveField(
            model_name='client',
            name='paid',
        ),
        migrations.RemoveField(
            model_name='client',
            name='payment_method',
        ),
        migrations.RemoveField(
            model_name='client',
            name='plan',
        ),
        migrations.AlterField(
            model_name='client',
            name='emergency_phone_number',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='client_membership',
            name='client',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='members.client'),
        ),
    ]
