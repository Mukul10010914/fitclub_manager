from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth, Group
from django.conf import settings
from django.contrib import messages
from .models import member, membership
from members.models import client, client_membership
from datetime import datetime
from datetime import date
import pandas as pd
import razorpay


def signup(request):
	if request.method == "POST":
		username = request.POST.get('username')
		firstname = request.POST.get('fname')
		lastname = request.POST.get('lname')
		email = request.POST.get('email')
		number = request.POST.get('number')
		address = request.POST.get('address')
		password = request.POST.get('password')

		g = Group.objects.get_or_create(name=username)
		my_group = Group.objects.get(name=username) 

		u = User.objects.create_user(username=username, password=password, email=email, first_name=firstname, last_name=lastname)

		u1 = User.objects.get(username=username)
		my_group.user_set.add(u1)
		m1 = member(member=u1, phone_number=number, address=address)
		m1.save()

		u2 = member.objects.get(member=u1)
		dtObj = date.today()
		n = 1
		future_date = dtObj + pd.DateOffset(months=n)
		m2 = membership(member=u2, due_date=future_date)
		m2.save()

		return redirect('/')

	else:
		return render(request, "signup.html", {})


def signin(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = auth.authenticate(username=username, password=password)

		if user is not None:
			auth.login(request, user)
			return redirect('/Welcome/')

		else:
			messages.info(request,'INVALID CREDENTIALS')
			return render(request, "signin.html", {})

	else:
		return render(request, "signin.html", {})


def welcome(request):
	if request.user.is_authenticated:
		m = member.objects.get(member=request.user.id)
		n = membership.objects.filter(member=m.id)

		w = n.order_by('-id')
		lw = n.last()

		d1 = date.today()
		d2 = lw.due_date
		f = "Null"
		if d1>d2:
			f=1

		my_group = Group.objects.get(name=request.user.username)
		data = client.objects.filter(gym=my_group)

		a = data.filter(active="True").count()
		b = data.filter(active="False").count()

		context = {'m':m, 'w':w, 'lw':lw, 'f':f, 'a':a, 'b':b}

		return render(request, "home1.html", context)
	else:
		return redirect('/LogIn/')

def renewal(request):
	return render(request, "renewal.html", {})

def payment(request):
	if request.method == "POST":
		plan = request.POST.get('membership_plan')

		if plan == "Basic":
			a = 700 * 100
		else:
			a = 1000 * 100

		keyid = 'rzp_test_yiOWNNyFRwA6SD'
		keySecret = 'HPkSUymDGbPH65bdojWQ25po'
		client = razorpay.Client(auth=(keyid, keySecret))
		payment = client.order.create({'amount': a, 'currency':'INR', 'payment_capture': '1'})

		return render(request, "payment.html", {'p':plan, 'pay':payment})
	else:
		return render(request, "payment.html", {})

def success(request):
	if request.method == "POST":
		a = request.POST
		p = request.POST.get('plan')
		m = member.objects.get(member=request.user.id)
		n = membership.objects.get(member=m)
		

		dtObj = date.today()
		n1 = 12
		future_date = dtObj + pd.DateOffset(months=n1)
		b = membership(member=m, due_date=future_date, paid="True", payment_id=a['razorpay_payment_id'])
		b.save()
		m.plan = p
		m.save()

		m1 = member.objects.get(member=request.user.id)
		n2 = membership.objects.get(member=m)
		return render(request, "success.html", {'a':a, 'm':m1, 'n':n2})
	else:
		return redirect('/Payment/')

def settings1(request):
	return render(request, "settings.html", {})

def logout(request):
	auth.logout(request)
	return redirect('/')

def chusername(request):
	uname = request.POST.get('new_user')
	u = request.user
	u.username = uname
	u.save()
	return redirect('/Settings/')

def chemail(request):
	id1 = request.POST.get('new_email_id')
	u = request.user
	u.email = id1
	u.save()
	return redirect('/Settings/')

def chaddress(request):
	a = request.POST.get('new_address')
	m = member.objects.get(member=request.user.id)
	m.address = a
	m.save()
	return redirect('/Settings/')

def chphonenumber(request):
	a = request.POST.get('new_phone_number')
	m = member.objects.get(member=request.user.id)
	m.phone_number = a
	m.save()
	return redirect('/Settings/')

def chpassword(request):
	p = request.POST.get('new_pass')
	u = request.user
	u.set_password(p)
	u.save()
	auth.logout(request)
	return redirect('/')