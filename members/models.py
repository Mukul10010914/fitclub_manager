from django.db import models
from django.db.models import Model
from django.db.models import Q
from django.contrib.auth.models import Group

# Create your models here.
class client(models.Model):
	gender = (
		('Male', 'Male'),
		('Female', 'Female'),
		('Other', 'Other'),
		)

	name = models.CharField(max_length=100)
	dob = models.DateField(blank=True)
	doa = models.DateField(default=None, blank=True, null=True)
	phone_number = models.BigIntegerField(unique=True)
	email = models.CharField(max_length=100, default=None)
	emergency_phone_number = models.CharField(blank=True, null=True, max_length=100)
	address = models.CharField(max_length=200)
	gender = models.CharField(max_length=100, choices=gender)
	mother_name = models.CharField(max_length=100, blank=True)
	father_name = models.CharField(max_length=100, blank=True)
	spouse_name = models.CharField(max_length=100, blank=True, null=True)
	gym = models.ForeignKey(Group, on_delete=models.CASCADE, default=None)
	profile_image = models.ImageField(upload_to='pics', blank=True)
	active = models.CharField(max_length=50, default="True")

	def __str__(self):
		return self.name


class client_membership(models.Model):
	membership_plan = (
		('Monthly', 'Monthly'),
		('Quaterly', 'Quaterly'),
		('Yearly', 'Yearly'),
		)

	payment = (
		('Cash', 'Cash'),
		('Online Payment', 'Online Payment'),
		)

	client = models.ForeignKey(client, on_delete=models.CASCADE, default=None)
	plan = models.CharField(max_length=100, choices=membership_plan, blank=True)
	due_date  = models.DateField(blank=True, default=None)
	amount = models.CharField(max_length=100, blank=True)
	discount = models.CharField(max_length=100, blank=True, null=True)
	final_amount = models.CharField(max_length=100, blank=True)
	payment_method = models.CharField(max_length=100, choices=payment, blank=True)
	date  = models.DateField(blank=True, default=None)
	paid = models.BooleanField(default=False)

	def __str__(self):
		return self.client.name + " - " + self.plan
