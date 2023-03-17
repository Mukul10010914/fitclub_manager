from django.db import models
from django.db.models import Model
from django.db.models import Q
from django.contrib.auth.models import User

# Create your models here.
class member(models.Model):
	membership_plan = (
		('Free', 'Free'),
		('Basic', 'Basic'),
		('Premium', 'Premium'),
		)
	member = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
	phone_number = models.BigIntegerField()
	plan=models.CharField(max_length=100, choices=membership_plan, default="Free")	
	address = models.CharField(max_length=200)

	def __str__(self):
		return self.member.username + " - " + self.plan

class membership(models.Model):
	payment_id = models.CharField(max_length=100, default="Free")
	paid = models.BooleanField(default=False)
	date  = models.DateField(auto_now_add=True)
	due_date  = models.DateField(blank=True)
	member = models.ForeignKey(member, on_delete=models.DO_NOTHING, default=None)

	def __str__(self):
		return "For " + self.member.member.username
