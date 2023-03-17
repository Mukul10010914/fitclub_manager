from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.conf import settings

def home(request):
	if request.user.is_authenticated:
		return redirect('/Welcome/')
	else:
		return render(request, "home.html", {})

def about(request):
	return render(request, "about.html", {})

def features(request):
	return render(request, "features.html", {})
