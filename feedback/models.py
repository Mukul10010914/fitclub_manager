from django.db import models
from django.db.models import Model
from django.db.models import Q
from django.contrib.auth.models import User
from gym_or_club.models import *
# Create your models here.
class query(models.Model):
	gym_or_club = models.CharField(max_length=100)
	phone_number = models.BigIntegerField()
	name = models.CharField(max_length=100)
	email = models.CharField(max_length=100)
	date  = models.DateField(auto_now_add=True, editable=False)

class review(models.Model):
	rating = models.IntegerField()
	comment = models.CharField(max_length=1000, blank=True, default=None)
	member = models.ForeignKey(User, on_delete=models.PROTECT, default=None)

	def __str__(self):
		return "By " + self.member.username
