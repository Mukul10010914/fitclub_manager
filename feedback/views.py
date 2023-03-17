from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.conf import settings
from .models import *
# Create your views here.
def contact(request):
	if request.method == "POST":
		name = request.POST.get('name')
		gym_or_club = request.POST.get('gym_or_club')
		email = request.POST.get('email')
		mobile = request.POST.get('mobile')

		q = query(name=name, gym_or_club=gym_or_club, email=email, phone_number=mobile)
		q.save()
		return redirect('/Contact/')

	else:
		return render(request, "contact.html", {})

def feedback(request):
	if request.method == "POST":
		rating = request.POST.get('rating')
		comment = request.POST.get('comment')
		user = User.objects.get(username=request.user.username)

		f = review(rating=rating, comment=comment, member=user)
		f.save()
		return redirect('/Member/')

	else:
		return render(request, "feedback.html", {})